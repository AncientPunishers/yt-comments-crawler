from src.video import Video

yt_url = "https://www.youtube.com/watch?v=AsWuKGZ1q7I" # 53 comments
yt_url = "https://www.youtube.com/watch?v=_F5aWL7Ac3k" # 233 comments
yt_url = "https://www.youtube.com/watch?v=0aoL0aAI18s" # 382 comments
# yt_url = "https://www.youtube.com/watch?v=gdZLi9oWNZg" # 15m comments
# yt_url = "https://www.youtube.com/watch?v=uRxsLwqx4VM"
# yt_url = "https://www.youtube.com/watch?v=IHNzOHi8sJs"


#
# init video
#
video = Video(yt_video_url=yt_url)

#
# print top level info about this video
#
print(video)

comments_request_url = video.get_video_comment_request_url()
video_comment_headers = video.get_video_comment_headers()
video_context = video.video_raw_context

#
# print all comments and replies for this video
#
for c in video.get_video_comments():
    print(c)
    if c.reply_count:
        for r in c.get_comment_replies(c.comment_id, comments_request_url, video_comment_headers, video_context):
            print(r)
