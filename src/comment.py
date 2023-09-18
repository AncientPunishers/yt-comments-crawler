from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Mapping, List, Optional

import requests

from src import utils

comment_output_blacklist = {'reply_initial_cont_token'}


@dataclass(repr=False)
class Comment:

    video_id: str
    author: str
    comment: List[str]
    comment_id: str
    like_count: int = 0
    reply_count: int = 0
    is_reply: bool = False
    parent_comment_id: str = ''
    published_date: str = ""
    crawled_date: datetime = datetime.now()
    is_video_owner: bool = False
    reply_initial_cont_token: str = ""

    def get_comment_replies(self,
                            parent_id: str,
                            comments_request_url: str,
                            video_comment_headers: Mapping,
                            video_context: str) -> Optional[List[Comment]]:
        replies = None
        replies_pagination_token = self.reply_initial_cont_token

        while replies_pagination_token:
            request_body = utils.comment_request_template(replies_pagination_token, video_context)
            resp = requests.post(comments_request_url, data=json.dumps(request_body), headers=video_comment_headers)

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
                            comment_id = commentRenderer['commentId']
                            for run in commentRenderer['contentText']['runs']:
                                comment.append(run['text'])

                            if 'voteCount' in commentRenderer:
                                like_count = commentRenderer['voteCount']['simpleText']

                            if 'authorIsChannelOwner' in commentRenderer:
                                authorIsChannelOwner = str(commentRenderer['authorIsChannelOwner']).lower() == 'true'

                            if 'publishedTimeText' in commentRenderer:
                                publishedTimeText = commentRenderer['publishedTimeText']['runs'][0]['text']

                            replies.append(
                                Comment(
                                    video_id=self.video_id,
                                    author=author,
                                    comment=comment,
                                    comment_id=comment_id,
                                    parent_comment_id=parent_id,
                                    like_count=like_count,
                                    reply_count=0,
                                    published_date=publishedTimeText,
                                    is_video_owner=authorIsChannelOwner,
                                    is_reply=True))
                else:
                    replies_pagination_token = ""

            if resp:
                resp.close()

        return replies

    def has_reply(self):
        return self.reply_count > 0

    def __str__(self):
        s = (
            f'{"        " if self.is_reply else ""}author:           {self.author}\n'
            f'{"        " if self.is_reply else ""}like count:       {self.like_count}\n'
            f'{"        " if self.is_reply else ""}reply count:      {self.reply_count}\n'
            f'{"        " if self.is_reply else ""}published date:   {self.published_date}\n'
            f'{"        " if self.is_reply else ""}crawled date:     {self.crawled_date.strftime("%Y-%d-%m")}\n'
            f'{"        " if self.is_reply else ""}comment:          {self.comment}\n'
        )
        return s
