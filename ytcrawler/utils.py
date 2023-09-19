import json
import random
from typing import MutableMapping

from ytcrawler.constants import USER_AGENTS, DEFAULT_HEADERS


def random_user_agent():
    return USER_AGENTS[random.randint(0, len(USER_AGENTS)-1)]


def yt_video_page_request_headers():
    return {
        **DEFAULT_HEADERS,
        'user-agent': random_user_agent(),
        'content-type': 'text/html; charset=utf-8',
    }


def yt_comment_request_headers(yt_video_url: str):
    return {
        "user-agent": random_user_agent(),
        "accept": "*/*",
        "host": "www.youtube.com",
        "referer": yt_video_url,
        "content-type": "application/json",
        "origin": "https://www.youtube.com",
        "X-Youtube-Bootstrap-Logged-In": "false",
        "X-Youtube-Client-Name": "1",
        "accept-language": "en-US,en;q=0.5",
    }


def comment_request_template(cont_token: str, context: str) -> MutableMapping[str, str]:
    return {
        "context": json.loads(context),
        "continuation": cont_token
    }


def print_comments(video, json_encoder, limit: int, print_replies: bool = False):
    comment_generator = video.get_video_comments()
    req_url = video.get_video_comment_request_url()
    comment_hdrs = video.get_video_comment_headers()
    video_context = video.video_raw_context

    while limit != 0:
        try:
            comment = next(comment_generator)
            print(json_encoder(comment))
            if comment.has_reply() and print_replies:
                for r in comment.get_comment_replies(comment.comment_id, req_url, comment_hdrs, video_context):
                    print(json_encoder(r))
                    limit -= 1
                    if limit == 0:
                        return
            limit -= 1
        except StopIteration:
            break
