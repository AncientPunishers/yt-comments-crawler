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
                comment: List[str],
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
        replies_pagination_token = self.reply_initial_cont_token

        while replies_pagination_token:
            request_body = Comment.comment_request_template(replies_pagination_token, video_context)
            resp = requests.post(api_url, data=json.dumps(request_body), headers=headers)

            if resp.status_code == 200:
                replies = []
                res = json.loads(resp.content.decode('utf-8'))

                # cont items could be missing if reply thread were deleted for whatever reasons
                if 'continuationItems' in res['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']:

                    continuationItems = \
                        res['onResponseReceivedEndpoints'][0]['appendContinuationItemsAction']['continuationItems']

                    if 'continuationItemRenderer' in continuationItems[-1]:
                        replies_pagination_token = \
                            continuationItems[-1]['continuationItemRenderer']['button']['buttonRenderer']['command'][
                            'continuationCommand']['token']
                    else:
                        replies_pagination_token = ""

                    for continuationItem in continuationItems:
                        author, comment, like_count, authorIsChannelOwner, publishedTimeText = "", [], 0, False, ""

                        if 'commentRenderer' in continuationItem:
                            commentRenderer = continuationItem['commentRenderer']
                            author = commentRenderer['authorText']['simpleText']
                            for run in commentRenderer['contentText']['runs']:
                                comment.append(run['text'])

                            if 'voteCount' in commentRenderer:
                                like_count = commentRenderer['voteCount']['simpleText']

                            if 'authorIsChannelOwner' in commentRenderer:
                                authorIsChannelOwner = str(commentRenderer['authorIsChannelOwner']).lower() == 'true'

                            if 'publishedTimeText' in commentRenderer:
                                publishedTimeText = commentRenderer['publishedTimeText']['runs'][0]['text']

                            replies.append(Comment(author, comment, like_count, 0, publishedTimeText, authorIsChannelOwner))
                else:
                    replies_pagination_token = ""

            # done
            # time.sleep(random.randint(0, 2))
            if resp:
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
            f'author:           {self.author}\n'
            f'like count:       {self.like_count}\n'
            f'reply count:      {self.reply_count}\n'
            f'published date:   {self.published_date}\n'
            f'crawled date:     {self.crawled_date.strftime("%Y-%d-%m")}\n'
            f'comment:          {self.comment}\n'
        )
        return s

    def replies_str(self):
        s = (
            f'\tauthor:         {self.author}\n'
            f'\tlike count:     {self.like_count}\n'
            f'\treply count:    {self.reply_count}\n'
            f'\tpublished date: {self.published_date}\n'
            f'\tcrawled date:   {self.crawled_date.strftime("%Y-%d-%m")}\n'
            f'\tcomment:        {self.comment}\n'
        )
        return s
