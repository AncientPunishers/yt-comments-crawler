import json
import re
from typing import Optional, Mapping, Iterator

import requests

from src import utils
from src.comment import Comment
from src.urls import YOUTUBE_VIDEO_API_URL_FORMAT

# regex patterns to parse video specific information from video's raw html page
VIDEO_ID_PATTERN = re.compile('https:\/\/www.youtube.com\/watch.*v=([a-zA-Z0-9_-]+).*')
INNERTUBE_KEY_PATTERN = re.compile('INNERTUBE_API_KEY":"([a-zA-Z_1-9]+)\"')
INNERTUBE_API_VERSION_PATTERN = re.compile('INNERTUBE_API_VERSION":"([a-zA-Z_1-9]+)"')
INNERTUBE_CLIENT_VERSION_PATTERN = re.compile('INNERTUBE_CLIENT_VERSION":"([0-9\\.]+)"')
CONTINUATION_TOKEN_PATTERN = re.compile('continuationCommand":{"token":"([a-zA-Z0-9%]+)"')
INNERTUBE_CONTEXT_PATTERN = re.compile('"INNERTUBE_CONTEXT":(.*?}}),')
VIDEO_AUTHOR_PATTERN = re.compile(',"author":"(.+?)","')
VIDEO_AUTHOR_SUBSCRIBER_COUNT_PATTERN = re.compile('simpleText":"([0-9MKB.]+) subscribers"')
VIDEO_TITLE_PATTERN = re.compile('"videoDescriptionHeaderRenderer":{"title":{"runs":\[{"text":"(.+?)"}]},')
VIDEO_VIEW_COUNT_PATTERN = re.compile('"videoViewCountRenderer":{"viewCount":{"simpleText":"(.+?) views"},"shortViewCount":{"simpleText":"([0-9MKB.]+) views"},')
VIDEO_PUBLISHED_DATE_PATTERN = re.compile('dateText":{"simpleText":"(.+?)"},')
VIDEO_TOTAL_COMMENT_COUNT_PATTERN = re.compile('\"commentCount\":\{\"simpleText\":\"(.+?)\"},\"contentRenderer\"')


class Video:

    def __init__(self,
                 yt_video_url: str,
                 yt_video_id: str = "",
                 yt_html_body: str = "",
                 yt_video_innertube_key: str = "",
                 yt_video_initial_continuation_key: str = "",
                 yt_video_raw_context: str = "",
                 yt_video_author_name: str = "",
                 yt_video_subscriber_count: str = "",
                 yt_video_view_exact_count: str = "",
                 yt_video_published_date: str = "",
                 yt_video_title: str = "",
                 yt_video_client_ver: str = ""):

        if not yt_html_body:
            yt_html_body = Video.retrieve_video_body(yt_video_url)

        self.video_url = yt_video_url
        self.video_id = yt_video_id
        self.html_body = yt_html_body
        self.video_innertube_key = yt_video_innertube_key
        self.video_initial_continuation_key = yt_video_initial_continuation_key
        self.video_raw_context = yt_video_raw_context
        self.total_comment_count = None
        self.author_name = yt_video_author_name
        self.video_title = yt_video_title
        self.video_subscriber_count = yt_video_subscriber_count
        self.video_view_exact_count = yt_video_view_exact_count
        self.video_publish_date = yt_video_published_date
        self.video_client_version = yt_video_client_ver
        self.seen_continuation_tokens = []

        if not self.video_id:
            self.video_id = Video.parse_video_id_from_url(self.video_url)

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
        return YOUTUBE_VIDEO_API_URL_FORMAT.\
            format(innertube_key=self.video_innertube_key,
                   pretty_print=str(pretty_print).lower())

    def get_video_comment_headers(self) -> Mapping:
        return utils.yt_comment_request_headers(self.video_url)

    def get_video_comments(self, comment_headers: Optional[Mapping] = None) -> Iterator[Comment]:
        initial_request = True
        pagination_token = self.video_continuation_key
        comments_request_url = self.get_video_comment_request_url()

        if not comment_headers:
            comment_headers = utils.yt_comment_request_headers(self.video_url)

        while pagination_token:

            continutionItemRenderer = []
            comment_request_body = utils.comment_request_template(pagination_token, self.video_raw_context)
            r = requests.post(comments_request_url, data=json.dumps(comment_request_body),
                              headers=comment_headers)
            res = json.loads(r.content)

            for commentThreadRenderer in res['onResponseReceivedEndpoints'][1 if initial_request else 0][
                'reloadContinuationItemsCommand' if initial_request else 'appendContinuationItemsAction'][
                'continuationItems']:
                initial_request = False
                author, comment, like_count, reply_count, publishedTimeText, authorIsChannelOwner, reply_cont_token = '', [], 0, 0, '', False, ""
                if 'commentThreadRenderer' in commentThreadRenderer:
                    commentRenderer = commentThreadRenderer['commentThreadRenderer']['comment']['commentRenderer']
                    author = commentRenderer['authorText']['simpleText']
                    comment_id = commentRenderer['commentId']
                    for run in commentRenderer['contentText']['runs']:
                        comment.append(run['text'])

                    if 'voteCount' in commentRenderer:
                        like_count = commentRenderer['voteCount']['simpleText']
                        if like_count.isdigit():
                            like_count = int(like_count)

                    if 'replyCount' in commentRenderer:
                        reply_count = commentRenderer['replyCount']
                        if type(reply_count) == str and reply_count.isdigit():
                            reply_count = int(reply_count)
                        if reply_count > 0:
                            reply_cont_token = \
                                commentThreadRenderer['commentThreadRenderer']['replies']['commentRepliesRenderer'][
                                    'contents'][
                                    0]['continuationItemRenderer']['continuationEndpoint']['continuationCommand'][
                                    'token']

                    authorIsChannelOwner = False
                    if 'authorIsChannelOwner' in commentRenderer:
                        authorIsChannelOwner = str(commentRenderer['authorIsChannelOwner']).lower() == 'true'

                    if 'publishedTimeText' in commentRenderer:
                        publishedTimeText = commentRenderer['publishedTimeText']['runs'][0]['text']

                    yield Comment(
                        video_id=self.video_id,
                        author=author,
                        comment_id=comment_id,
                        comment=comment,
                        like_count=like_count,
                        reply_count=reply_count,
                        published_date=publishedTimeText,
                        is_video_owner=authorIsChannelOwner,
                        reply_initial_cont_token=reply_cont_token)
                else:
                    continutionItemRenderer.append(commentThreadRenderer)

            # check for more comments
            pagination_token = ""
            if continutionItemRenderer:
                pagination_token = \
                    continutionItemRenderer[0]['continuationItemRenderer']['continuationEndpoint'][
                        'continuationCommand'][
                        'token']

    def asdict(self) -> Mapping:
        return {
            'title': self.video_title,
            'author': self.author_name,
            'view': self.video_view_count,
            'comments': self.total_comment_count,
            'published_date': self.video_publish_date,
            'url': self.video_url,
            'id': self.video_id,
        }

    @staticmethod
    def retrieve_video_body(yt_video_url: str, headers: Optional[Mapping] = None) -> str:
        if not headers:
            headers = utils.yt_video_page_request_headers()

        resp = requests.get(yt_video_url, headers=headers)
        if resp.status_code != 200:
            raise Exception('Failed: retrieve video html body', resp.content)

        body = resp.content.decode('utf-8')
        resp.close()
        return body

    @staticmethod
    def parse_video_id_from_url(url: str) -> Optional[str]:
        id = None
        matches = VIDEO_ID_PATTERN.findall(url)
        if matches:
            id = matches.pop()

        return id

    @staticmethod
    def parse_innertube_key_from_html(body: str) -> Optional[str]:
        key = None
        matches = INNERTUBE_KEY_PATTERN.findall(body)
        if matches:
            key = matches.pop()

        return key

    @staticmethod
    def parse_continuation_key_from_html(body: str) -> Optional[str]:
        key = None
        matches = CONTINUATION_TOKEN_PATTERN.findall(body)
        if matches:
            key = matches.pop()

        return key

    @staticmethod
    def parse_innertube_context_from_html(body: str) -> Optional[str]:
        context = None
        matches = INNERTUBE_CONTEXT_PATTERN.findall(body)
        if matches:
            context = matches.pop()

        return context

    @staticmethod
    def parse_video_author_name_from_html(body: str) -> Optional[str]:
        name = None
        matches = VIDEO_AUTHOR_PATTERN.findall(body)
        if matches:
            name = matches.pop()

        return name

    @staticmethod
    def parse_video_title_from_html(body: str) -> Optional[str]:
        title = None
        matches = VIDEO_TITLE_PATTERN.findall(body)
        if matches:
            title = matches.pop()

        return title

    @staticmethod
    def parse_video_subscriber_count_from_html(body: str) -> Optional[str]:
        count = None
        matches = VIDEO_AUTHOR_SUBSCRIBER_COUNT_PATTERN.findall(body)
        if matches:
            count = matches.pop()

        return count

    @staticmethod
    def parse_video_view_count_from_html(body: str) -> Optional[str]:
        exact_count, simple_count = None, None
        matches = VIDEO_VIEW_COUNT_PATTERN.findall(body)
        if matches:
            exact_count, simple_count = matches.pop()

        return exact_count

    @staticmethod
    def parse_video_published_date_from_html(body: str) -> Optional[str]:
        dt = None
        matches = VIDEO_PUBLISHED_DATE_PATTERN.findall(body)
        if matches:
            dt = matches.pop()

        return dt

    @staticmethod
    def parse_video_total_comment_count_from_html(body: str) -> Optional[str]:
        count = ""
        matches = VIDEO_TOTAL_COMMENT_COUNT_PATTERN.findall(body)
        if matches:
            count = matches.pop()

        return count

    @staticmethod
    def parse_video_client_version_from_html(body: str) -> str:
        ver = ""
        matches = INNERTUBE_CLIENT_VERSION_PATTERN.findall(body)
        if matches:
            ver = matches.pop()

        return ver

    def __str__(self):
        return f'''
title:          {self.video_title}
author:         {self.author_name}
view:           {self.video_view_count}
comments:       {self.total_comment_count}
subsribers:     {self.video_subscriber_count}
published date: {self.video_publish_date}
url:            {self.video_url}
id:             {self.video_id}
'''
