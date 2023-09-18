from ytcrawler.video import Video

yt_url = "https://www.youtube.com/watch?v=1W8oWhctpQ8"

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
comments = []
for c in video.get_video_comments():
    if len(comments) > 10:
        break
    comments.append(c)
    if c.reply_count:
        for r in c.get_comment_replies(c.comment_id, comments_request_url, video_comment_headers, video_context):
            comments.append(r)
            if len(comments) > 10:
                break

for c in comments:
    print(c)
