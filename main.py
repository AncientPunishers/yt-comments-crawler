from src.video import Video

yt_url = "https://www.youtube.com/watch?v=aTxCDOWNvEw" # 2 comments
yt_url = "https://www.youtube.com/watch?v=y_F9-_DucJw" # 20 comments
yt_url = "https://www.youtube.com/watch?v=AsWuKGZ1q7I" # 53 comments
# yt_url = "https://www.youtube.com/watch?v=5N8RXM1Z-Gw"
# yt_url = "https://www.youtube.com/watch?v=_F5aWL7Ac3k" # 206
# yt_url = "https://www.youtube.com/watch?v=IEAYS_UyO60" # 573
# yt_url = "https://www.youtube.com/watch?v=0r-9WqyOMXc" # 534
# yt_url = "https://www.youtube.com/watch?v=UXZzyKTsBMw"
# yt_url = "https://www.youtube.com/watch?v=FHh697DSIxQ"
# yt_url = "https://www.youtube.com/watch?v=OQ2oOp040f0"
# yt_url = "https://www.youtube.com/watch?v=gdZLi9oWNZg" # 15m comments
# yt_url = "https://www.youtube.com/watch?v=uRxsLwqx4VM"
# yt_url = "https://www.youtube.com/watch?v=IHNzOHi8sJs"


#
# init video
#
video = Video(yt_video_url=yt_url)
print(video)
# print(video.html_body)
print()


#
# retrieve video comments
#
top_level_comments = video.get_video_comments()

comments_request_url = video.get_video_comment_request_url()
video_comment_headers = video.get_video_comment_headers()
video_context = video.video_raw_context

for c in top_level_comments:
    print(c)
    if c.reply_count:
        for r in c.get_comment_replies(comments_request_url, video_context, video_comment_headers):
            print(r)
