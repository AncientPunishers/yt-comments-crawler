from typing import Optional, Mapping
import requests
import re


class Video:

    YT_COMMENT_API_URL_FORMAT = \
        "https://www.youtube.com/youtubei/v1/next?key={innertube_key}&prettyPrint={pretty_print}"

    # regex patterns to parse video specific information from video's raw html page
    INNERTUBE_KEY_PATTERN = re.compile('INNERTUBE_API_KEY":"([a-zA-Z_1-9]+)\"')
    INNERTUBE_API_VERSION_PATTERN = re.compile('INNERTUBE_API_VERSION":"([a-zA-Z_1-9]+)"')
    INNERTUBE_CLIENT_VERSION_PATTERN = re.compile('INNERTUBE_CLIENT_VERSION":"([0-9\\.]+)"')
    CONTINUATION_TOKEN_PATTERN = re.compile('continuationCommand":{"token":"([a-zA-Z0-9%]+)"')
    INNERTUBE_CONTEXT_PATTERN = re.compile('"INNERTUBE_CONTEXT":(.*?}}),')
    VIDEO_AUTHOR_PATTERN = re.compile(',"author":"(.+?)","')
    VIDEO_AUTHOR_SUBSCRIBER_COUNT_PATTERN = re.compile('simpleText":"([0-9MK.]+) subscribers"')
    VIDEO_TITLE_PATTERN = re.compile('"videoDescriptionHeaderRenderer":{"title":{"runs":\[{"text":"(.+?)"}]},')
    VIDEO_VIEW_COUNT_PATTERN = re.compile('"videoViewCountRenderer":{"viewCount":{"simpleText":"(.+?) views"},"shortViewCount":{"simpleText":"([0-9MK.]+) views"},')
    VIDEO_PUBLISHED_DATE_PATTERN = re.compile('dateText":{"simpleText":"(.+?)"},')
    VIDEO_TOTAL_COMMENT_COUNT_PATTERN = re.compile('"commentCount":{"simpleText":"([0-9]+)"')

    def __init__(self,
                 yt_video_url: str,
                 yt_html_body: str,
                 yt_video_innertube_key: str = "",
                 yt_video_initial_continuation_key: str = "",
                 yt_video_raw_context: str = "",
                 yt_video_author_name: str = "",
                 yt_video_subscriber_count: str = "",
                 yt_video_view_exact_count: str = "",
                 yt_video_published_date: str = "",
                 yt_video_title: str = "",
                 yt_video_client_ver: str = ""):

        self.video_url = yt_video_url
        self.html_body = yt_html_body
        self.video_innertube_key = yt_video_innertube_key
        self.video_initial_continuation_key = yt_video_initial_continuation_key
        self.video_raw_context = yt_video_raw_context
        self.total_comment_count = 0
        self.author_name = yt_video_author_name
        self.video_title = yt_video_title
        self.video_subscriber_count = yt_video_subscriber_count
        self.video_view_exact_count = yt_video_view_exact_count
        self.video_publish_date = yt_video_published_date
        self.video_client_version = yt_video_client_ver
        self.seen_continuation_tokens = []

        if not self.html_body:
            raise Exception("Video: failed to retrieve raw html body")

        if not self.video_innertube_key:
            self.video_innertube_key = Video.parse_innertube_key_from_html(self.html_body)

        if not self.video_initial_continuation_key:
            self.video_continuation_key = Video.parse_continuation_key_from_html(self.html_body)

        if not self.total_comment_count:
            self.total_comment_count = Video.parse_video_total_comment_count_from_html(self.html_body)

        if not self.video_raw_context:
            self.video_raw_context = Video.parse_innertube_context_from_html(self.html_body)

        if not self.author_name:
            self.author_name = Video.parse_video_author_name_from_html(self.html_body)

        if not self.video_title:
            self.video_title = Video.parse_video_title_from_html(self.html_body)

        if not self.video_subscriber_count:
            self.video_subscriber_count = Video.parse_video_subscriber_count_from_html(self.html_body)

        if not self.video_view_exact_count:
            self.video_view_count = Video.parse_video_view_count_from_html(self.html_body)

        if not self.video_publish_date:
            self.video_publish_date = Video.parse_video_published_date_from_html(self.html_body)

        if not self.video_client_version:
            self.video_client_version = Video.parse_video_client_version_from_html(self.html_body)

        # populate first pagination key
        self.seen_continuation_tokens.append(self.video_continuation_key)

    def get_video_comment_request_url(self, pretty_print: bool = False):
        return Video.YT_COMMENT_API_URL_FORMAT.\
            format(innertube_key=self.video_innertube_key,
                   pretty_print=str(pretty_print).lower())

    @staticmethod
    def retrieve_video_body(yt_video_url: str, headers: Mapping) -> str:
        resp = requests.get(yt_video_url, headers=headers)
        if resp.status_code != 200:
            raise Exception('Failed: retrieve video html body', resp.content)

        body = resp.content.decode('utf-8')
        resp.close()
        return body

    @staticmethod
    def parse_innertube_key_from_html(body: str) -> Optional[str]:
        key = None
        matches = Video.INNERTUBE_KEY_PATTERN.findall(body)
        if matches:
            key = matches.pop()

        return key

    @staticmethod
    def parse_continuation_key_from_html(body: str) -> Optional[str]:
        key = None
        matches = Video.CONTINUATION_TOKEN_PATTERN.findall(body)
        if matches:
            key = matches.pop()

        return key

    @staticmethod
    def parse_innertube_context_from_html(body: str) -> Optional[str]:
        context = None
        matches = Video.INNERTUBE_CONTEXT_PATTERN.findall(body)
        if matches:
            context = matches.pop()

        return context

    @staticmethod
    def parse_video_author_name_from_html(body: str) -> Optional[str]:
        name = None
        matches = Video.VIDEO_AUTHOR_PATTERN.findall(body)
        if matches:
            name = matches.pop()

        return name

    @staticmethod
    def parse_video_title_from_html(body: str) -> Optional[str]:
        title = None
        matches = Video.VIDEO_TITLE_PATTERN.findall(body)
        if matches:
            title = matches.pop()

        return title

    @staticmethod
    def parse_video_subscriber_count_from_html(body: str) -> Optional[str]:
        count = None
        matches = Video.VIDEO_AUTHOR_SUBSCRIBER_COUNT_PATTERN.findall(body)
        if matches:
            count = matches.pop()

        return count

    @staticmethod
    def parse_video_view_count_from_html(body: str) -> Optional[str]:
        exact_count, simple_count = None, None
        matches = Video.VIDEO_VIEW_COUNT_PATTERN.findall(body)
        if matches:
            exact_count, simple_count = matches.pop()

        return exact_count

    @staticmethod
    def parse_video_published_date_from_html(body: str) -> Optional[str]:
        dt = None
        matches = Video.VIDEO_PUBLISHED_DATE_PATTERN.findall(body)
        if matches:
            dt = matches.pop()

        return dt

    @staticmethod
    def parse_video_total_comment_count_from_html(body: str) -> Optional[int]:
        count = -1
        matches = Video.VIDEO_TOTAL_COMMENT_COUNT_PATTERN.findall(body)
        if matches:
            raw_count = matches.pop()
            if raw_count.isdigit():
                count = int(raw_count)

        return count

    @staticmethod
    def parse_video_client_version_from_html(body: str) -> str:
        ver = ""
        matches = Video.INNERTUBE_CLIENT_VERSION_PATTERN.findall(body)
        if matches:
            ver = matches.pop()

        return ver

    def __str__(self):
        return f'''
title: {self.video_title}
author: {self.author_name}
view: {self.video_view_count}
comments: {self.total_comment_count}
sub count: {self.video_subscriber_count}
published_date: {self.video_publish_date}
url: {self.video_url}
initial_cont_key: {self.video_continuation_key}
'''
