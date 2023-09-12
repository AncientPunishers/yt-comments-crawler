from src.video import Video
from src.comment import Comment

import random

yt_url = "https://www.youtube.com/watch?v=aTxCDOWNvEw" # 2 comments
yt_url = "https://www.youtube.com/watch?v=y_F9-_DucJw" # 20 comments
# yt_url = "https://www.youtube.com/watch?v=AsWuKGZ1q7I" # 53 comments
yt_url = "https://www.youtube.com/watch?v=5N8RXM1Z-Gw"
# yt_url = "https://www.youtube.com/watch?v=_F5aWL7Ac3k" # 206
# yt_url = "https://www.youtube.com/watch?v=IEAYS_UyO60" # 573
# yt_url = "https://www.youtube.com/watch?v=0r-9WqyOMXc" # 534
# yt_url = "https://www.youtube.com/watch?v=UXZzyKTsBMw"
# yt_url = "https://www.youtube.com/watch?v=FHh697DSIxQ"
# yt_url = "https://www.youtube.com/watch?v=OQ2oOp040f0"
# yt_url = "https://www.youtube.com/watch?v=gdZLi9oWNZg" # 15m comments
# yt_url = "https://www.youtube.com/watch?v=uRxsLwqx4VM"
# yt_url = "https://www.youtube.com/watch?v=IHNzOHi8sJs"


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
yt_video_html_body = Video.retrieve_video_body(yt_url, yt_page_request_headers)

#
# build video
#
video = Video(yt_video_url=yt_url, yt_html_body=yt_video_html_body)
print(video)
# print(video.html_body)
print()


#
# retrieve video comments
#
top_level_comments = video.get_video_comments(default_comment_headers)

comments_request_url = video.get_video_comment_request_url()
for c in top_level_comments:
    print(c)
    if c.reply_count:
        for r in c.get_comment_replies(comments_request_url, default_comment_headers, video.video_raw_context):
            print(r)
