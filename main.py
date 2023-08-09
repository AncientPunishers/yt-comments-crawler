from src.video import Video
from src.comment import Comment

import requests
import re
import json
import time
import random
from datetime import datetime

# yt_url = "https://www.youtube./watch?v=aTxCDOWNvEw" # 2 comments
# yt_url = "https://www.youtube.com/watch?v=y_F9-_DucJw" # 20 comments
yt_url = "https://www.youtube.com/watch?v=AsWuKGZ1q7I" # 53 comments
# yt_url = "https://www.youtube.com/watch?v=_F5aWL7Ac3k" # 206
# yt_url = "https://www.youtube.com/watch?v=IEAYS_UyO60" # 573
# yt_url = "https://www.youtube.com/watch?v=0r-9WqyOMXc" # 534
# yt_url = "https://www.youtube.com/watch?v=UXZzyKTsBMw"
# yt_url = "https://www.youtube.com/watch?v=FHh697DSIxQ"


common_user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
]
selected_user_agent = common_user_agents[random.randint(0, len(common_user_agents)-1)]

yt_page_request_headers = {
    "user-agent": selected_user_agent,
    "accept": "*/*",
    "content-type": "text/html; charset=utf-8",
}

default_comment_headers = {
        "user-agent": selected_user_agent,
        "accept": "*/*",
        "host": "www.youtube.com",
        "referer": yt_url,
        "content-type": "application/json",
        "origin": "https://www.youtube.com",
        "X-Youtube-Bootstrap-Logged-In": "false",
        "X-Youtube-Client-Name": "1",
         "accept-language": "en-US,en;q=0.5",
    }

#
# get video html body
#
# yt_video_html_body = ""
# resp = requests.get(yt_url, headers=yt_page_request_headers)
# if resp.status_code != 200:
#     raise Exception('main: failed get video html body')
# else:
#     yt_video_html_body = resp.content.decode("utf-8")

yt_video_html_body = Video.retrieve_video_body(yt_url, yt_page_request_headers)

#
# build video
#
video = Video(yt_video_url=yt_url, yt_html_body=yt_video_html_body)

#
# retrieve video comments
#
initial_request = True
top_lvl_comments = []
pagination_token = video.video_continuation_key
comments_request_url = video.get_video_comment_request_url()

while pagination_token:

    continutionItemRenderer = []
    comment_request_body = Comment.comment_request_template(pagination_token, video.video_raw_context)
    time.sleep(random.randint(0, 2))
    r = requests.post(comments_request_url, data=json.dumps(comment_request_body), headers=default_comment_headers)
    res = json.loads(r.content)
    time.sleep(random.randint(0, 2))
    r.close()

    for commentThreadRenderer in res['onResponseReceivedEndpoints'][1 if initial_request else 0]['reloadContinuationItemsCommand' if initial_request else 'appendContinuationItemsAction']['continuationItems']:
        initial_request = False
        author, comment, like_count, reply_count, publishedTimeText, authorIsChannelOwner, reply_cont_token = '', '', 0, 0, '', False, ""
        if 'commentThreadRenderer' in commentThreadRenderer:
            commentRenderer = commentThreadRenderer['commentThreadRenderer']['comment']['commentRenderer']
            author = commentRenderer['authorText']['simpleText']
            for run in commentRenderer['contentText']['runs']:
                comment += run['text'] + ' '

            if 'voteCount' in commentRenderer:
                like_count = commentRenderer['voteCount']['simpleText']
                if like_count.isdigit():
                    like_count = int(like_count)

            if 'replyCount' in commentRenderer:
                reply_count = commentRenderer['replyCount']
                if type(reply_count) == str and reply_count.isdigit():
                    reply_count = int(reply_count)
                if reply_count > 0:
                    reply_cont_token = commentThreadRenderer['commentThreadRenderer']['replies']['commentRepliesRenderer']['contents'][0]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

            authorIsChannelOwner = False
            if 'authorIsChannelOwner' in commentRenderer:
                authorIsChannelOwner = str(commentRenderer['authorIsChannelOwner']).lower() == 'true'

            if 'publishedTimeText' in commentRenderer:
                publishedTimeText = commentRenderer['publishedTimeText']['runs'][0]['text']

            top_lvl_comments.append(Comment(author, comment, like_count, reply_count, publishedTimeText, authorIsChannelOwner, reply_cont_token))
        else:
            continutionItemRenderer.append(commentThreadRenderer)

    # check for more comments
    pagination_token = ""
    if continutionItemRenderer:
        pagination_token = continutionItemRenderer[0]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']

print(video)
print()
for c in top_lvl_comments:
    print(c)
    if c.reply_count:
        for r in c.get_comment_replies(comments_request_url, default_comment_headers, video.video_raw_context):
            print(r.replies_str())
