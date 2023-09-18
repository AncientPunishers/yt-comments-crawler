YOUTUBE_VIDEO_API_URL = "https://www.youtube.com/youtubei/v1/next?key={innertube_key}&prettyPrint={pretty_print}"

DEFAULT_HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.5',
    'content-type': 'text/html; charset=utf-8',
    'host': 'www.youtube.com',
    'origin': 'www.youtube.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'same-origin',
    'Sec-Fetch-Site': 'same-origin',
    'X-Youtube-Bootstrap-Logged-In': 'false',
    'X-Youtube-Client-Name': '1',
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
]
