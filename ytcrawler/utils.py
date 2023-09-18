import json
import random
from typing import Mapping

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


def comment_request_template(cont_token: str, context: str) -> Mapping:
    return {
        "context": json.loads(context),
        "continuation": cont_token
    }
