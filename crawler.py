#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

from ytcrawler import Video, serialize


def main():
    parser = argparse.ArgumentParser(
        description='Python Youtube Video Comments Crawler as a command-line tool')
    parser.add_argument('url', help='The Youtube video url you want to crawl.')
    parser.add_argument('-debug', '--debug', action='store_true', default=False,
        help='debug mode')
    parser.add_argument('-c', '--comment', action='store_true', default=False,
        help='output comments only')
    parser.add_argument('-r', '--reply', action='store_true', default=False,
        help='output comments and replies')
    parser.add_argument('-p', '--pretty', action='store_true', default=False,
        help='pretty print all outputs')
    parser.add_argument('-v', '--video', action='store_true', default=False,
        help='output video info only')

    args = parser.parse_args()

    video = Video(args.url)
    comments_request_url = video.get_video_comment_request_url()
    video_comment_headers = video.get_video_comment_headers()
    video_context = video.video_raw_context
    json_encoder = serialize.PrettyJsonEncoder if args.pretty else serialize.DefaultExportJsonEncoder

    if args.debug:
        print(video)
        for comment in video.get_video_comments():
            print(comment)
            if comment.has_reply():
                for reply in comment.get_comment_replies(comment.comment_id, comments_request_url, video_comment_headers, video_context):
                    print(reply)
    elif args.comment:
        for comment in video.get_video_comments():
            print(json_encoder.encode(comment))
            if args.reply and comment.has_reply():
                for reply in comment.get_comment_replies(comment.comment_id, comments_request_url, video_comment_headers, video_context):
                    print(json_encoder.encode(reply))
    elif args.video:
        print(json_encoder.encode(video))


if __name__ == '__main__':
    main()
