#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

from ytcrawler import Video, serialize
from ytcrawler import utils


def main():
    parser = argparse.ArgumentParser(description='YouTube Video Comments Crawler')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-d', '--debug', action='store_true', help='Debug mode')
    parser.add_argument('-c', '--comment', action='store_true', help='Output comments only')
    parser.add_argument('-r', '--reply', action='store_true', help='Output comments and replies')
    parser.add_argument('-p', '--pretty', action='store_true', help='Pretty print all outputs')
    parser.add_argument('-v', '--video', action='store_true', help='Output video info only')
    parser.add_argument('-l', '--limit', type=int, default=10, help='Comment limit (default: 10)')
    args = parser.parse_args()

    video = Video(args.url)
    json_encoder = serialize.PrettyJsonEncoder if args.pretty else serialize.DefaultExportJsonEncoder
    limit = args.limit

    if args.debug:
        print(video)
        utils.print_comments(video, str, limit, print_replies=args.reply)
    elif args.comment or args.reply:
        utils.print_comments(video, json_encoder.encode, limit, print_replies=args.reply)
    elif args.video:
        print(json_encoder.encode(video))


if __name__ == '__main__':
    main()
