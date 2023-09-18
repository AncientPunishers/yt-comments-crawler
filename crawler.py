#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

from ytcrawler import Video, serialize


def check_comment_limit(cur: int, limit: int) -> bool:
    return False if limit < 0 else cur >= limit


def main():
    parser = argparse.ArgumentParser(description='Python Youtube Video Comments Crawler as a command-line tool')
    parser.add_argument('url', help='The Youtube video url you want to crawl.')
    parser.add_argument('-debug', '--debug', action='store_true', default=False, help='debug mode')
    parser.add_argument('-c', '--comment', action='store_true', default=False, help='output comments only')
    parser.add_argument('-r', '--reply', action='store_true', default=False, help='output comments and replies')
    parser.add_argument('-p', '--pretty', action='store_true', default=False, help='pretty print all outputs')
    parser.add_argument('-v', '--video', action='store_true', default=False, help='output video info only')
    parser.add_argument('-l', '--limit', type=int, default=-1,
                        help='number of video comments to return. default -1, return all.')

    args = parser.parse_args()

    video = Video(args.url)
    comments_request_url = video.get_video_comment_request_url()
    video_comment_headers = video.get_video_comment_headers()
    video_context = video.video_raw_context
    json_encoder = serialize.PrettyJsonEncoder if args.pretty else serialize.DefaultExportJsonEncoder

    # comment limit
    count = 0
    limit = args.limit

    if args.debug:
        print(video)
        for comment in video.get_video_comments():
            print(comment)
            count += 1
            if check_comment_limit(count, limit):
                return
            if comment.has_reply():
                for reply in comment.get_comment_replies(
                        comment.comment_id, comments_request_url, video_comment_headers, video_context):
                    print(reply)
                    count += 1
                    if check_comment_limit(count, limit):
                        return
    elif args.comment or args.reply:
        for comment in video.get_video_comments():
            print(json_encoder.encode(comment))
            count += 1
            if check_comment_limit(count, limit):
                return
            if args.reply and comment.has_reply():
                for reply in comment.get_comment_replies(
                        comment.comment_id, comments_request_url, video_comment_headers, video_context):
                    print(json_encoder.encode(reply))
                    count += 1
                    if check_comment_limit(count, limit):
                        return
    elif args.video:
        print(json_encoder.encode(video))


if __name__ == '__main__':
    main()
