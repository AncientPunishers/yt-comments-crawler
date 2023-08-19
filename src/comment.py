from __future__ import annotations

import json
import random
import time

import requests
from datetime import datetime
from typing import Mapping, List, Optional


class Comment:

    def __init__(self,
                author: str,
                comment: str,
                like_count: int = 0,
                reply_count: int = 0,
                published_date: str = "",
                is_video_owner: bool = False,
                reply_initial_cont_token: str = "",
                crawled_date: datetime = None,
                comment_detect_language: str = ""):

        self.author = author
        self.comment = comment
        self.like_count = like_count
        self.reply_count = reply_count
        self.published_date = published_date
        self.crawled_date = crawled_date or datetime.now()
        self.is_video_owner = is_video_owner
        self.reply_initial_cont_token = reply_initial_cont_token
        self.comment_detect_language = comment_detect_language

    def get_comment_replies(self, api_url: str, headers: Mapping, video_context: str) -> Optional[List[Comment]]:
        replies = None
        request_body = Comment.comment_request_template(self.reply_initial_cont_token, video_context)
        resp = requests.post(api_url, data=json.dumps(request_body), headers=headers)

        if resp.status_code == 200:
            replies = []
            res = json.loads(resp.content.decode('utf-8'))
            continuationItems = \
                res['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems']
            for continuationItem in continuationItems:
                author, comment, like_count, authorIsChannelOwner, publishedTimeText = "", "", 0, False, ""

                commentRenderer = continuationItem['commentRenderer']
                author = commentRenderer['authorText']['simpleText']
                for run in commentRenderer['contentText']['runs']:
                    comment += run['text'] + '\n'

                if 'voteCount' in commentRenderer:
                    like_count = commentRenderer['voteCount']['simpleText']

                if 'authorIsChannelOwner' in commentRenderer:
                    authorIsChannelOwner = str(commentRenderer['authorIsChannelOwner']).lower() == 'true'

                if 'publishedTimeText' in commentRenderer:
                    publishedTimeText = commentRenderer['publishedTimeText']['runs'][0]['text']

                replies.append(Comment(author, comment, like_count, 0, publishedTimeText, authorIsChannelOwner))

        # done
        time.sleep(random.randint(0, 2))
        resp.close()
        return replies

    @staticmethod
    def comment_request_template(cont_token: str, context: str) -> Mapping:
        return {
            "context": json.loads(context),
            "continuation": cont_token
        }

    def __str__(self):
        s = (
            f'author: {self.author}\n'
            f'like_count: {self.like_count}\n'
            f'reply_count: {self.reply_count}\n'
            f'published_date: {self.published_date}\n'
            f'crawled_date: {self.crawled_date.strftime("%Y-%d-%m")}\n'
            f'comment: {self.comment}\n'
        )
        return s

    def replies_str(self):
        s = (
            f'\tauthor: {self.author}\n'
            f'\tlike_count: {self.like_count}\n'
            f'\treply_count: {self.reply_count}\n'
            f'\tpublished_date: {self.published_date}\n'
            f'\tcrawled_date: {self.crawled_date.strftime("%Y-%d-%m")}\n'
            f'\tcomment: \n\t\t{self.comment}\n'
        )
        return s
