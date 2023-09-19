## Simple Comments Crawler for Youtube Video

* crawl yt video comments and replies using only the Python3 standard library.
* zero external dependency needed.

---

### > <b>__Video Info__</b>

```cli
# cli output prettify video json
./crawler.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -vp
```

```json
{
    "author": "Rick Astley",
    "comments": "2.3M",
    "id": "dQw4w9WgXcQ",
    "published_date": "Oct 24, 2009",
    "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)",
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "view": "1,448,440,882"
}
```

```cli
# cli output video json
./crawler.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -v
```
```json
{"author": "Rick Astley", "comments": "2.3M", "id": "dQw4w9WgXcQ", "published_date": "Oct 24, 2009", "title": "Rick Astley - Never Gonna Give You Up (Official Music Video)", "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "view": "1,448,441,673"}
```

---

### > <b>__Comment and Reply__</b>

```cli
# pretty comment
./crawler.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -cp -l 1
```
```json
{
    "author": "@RickAstleyYT",
    "comment": [
        "1 BILLION views for Never Gonna Give You Up!  Amazing, crazy, wonderful! Rick ",
        "♥",
        "️"
    ],
    "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg",
    "crawled_date": "2023-09-18T02:33:48.679423",
    "is_reply": false,
    "is_video_owner": true,
    "like_count": "1.2M",
    "parent_comment_id": "",
    "published_date": "2 years ago",
    "reply_count": 497,
    "video_id": "dQw4w9WgXcQ"
}
```

```cli
# get 4 comments only [replies are ignored]
./crawler.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -c -l 4
```

```json
{"video_id": "dQw4w9WgXcQ", "author": "@RickAstleyYT", "comment": ["1 BILLION views for Never Gonna Give You Up!  Amazing, crazy, wonderful! Rick ", "♥", "️"], "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg", "like_count": "1.2M", "reply_count": 497, "is_reply": false, "parent_comment_id": "", "published_date": "2 years ago", "crawled_date": "2023-09-18T02:28:13.900548", "is_video_owner": true}
{"video_id": "dQw4w9WgXcQ", "author": "@TheHoneyBoy", "comment": ["When someone like this comment i'll rewatch this video again"], "comment_id": "Ugzpq5TBzTd_fc1bwep4AaABAg", "like_count": "1.7K", "reply_count": 86, "is_reply": false, "parent_comment_id": "", "published_date": "1 day ago", "crawled_date": "2023-09-18T02:28:13.900548", "is_video_owner": false}
{"video_id": "dQw4w9WgXcQ", "author": "@raga.8950", "comment": ["We got rickrolled so many times that we don't even care anymore"], "comment_id": "Ugzl037LSf7KXBGIspp4AaABAg", "like_count": "263K", "reply_count": 495, "is_reply": false, "parent_comment_id": "", "published_date": "3 years ago (edited)", "crawled_date": "2023-09-18T02:28:13.900548", "is_video_owner": false}
{"video_id": "dQw4w9WgXcQ", "author": "@alvin-lvl84", "comment": ["No matter how many years pass, this song will always sound. The atmosphere of the 80s still remains. A true masterpiece"], "comment_id": "UgylcgKYqzXuKR1VavZ4AaABAg", "like_count": 667, "reply_count": 13, "is_reply": false, "parent_comment_id": "", "published_date": "5 days ago", "crawled_date": "2023-09-18T02:28:13.900548", "is_video_owner": false}
```

```cli
# get comments and replies, set limit just 10 (comments + replies)
./crawler.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -cr -l 10
```

```json
{"video_id": "dQw4w9WgXcQ", "author": "@RickAstleyYT", "comment": ["1 BILLION views for Never Gonna Give You Up!  Amazing, crazy, wonderful! Rick ", "♥", "️"], "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg", "like_count": "1.2M", "reply_count": 497, "is_reply": false, "parent_comment_id": "", "published_date": "2 years ago", "crawled_date": "2023-09-18T02:31:29.264043", "is_video_owner": true}
{"video_id": "dQw4w9WgXcQ", "author": "@25mxfu", "comment": ["cool"], "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg.9QM9WCCnud69QM9Xt-Bv-i", "like_count": "137K", "reply_count": 0, "is_reply": true, "parent_comment_id": "UgzarqjaaPC7TbFINNx4AaABAg", "published_date": "2 years ago (edited)", "crawled_date": "2023-09-18T02:31:29.264043", "is_video_owner": false}
{"video_id": "dQw4w9WgXcQ", "author": "@dan_shercat", "comment": ["You are the king of memes"], "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg.9QM9WCCnud69QM9Y00WCrh", "like_count": "90K", "reply_count": 0, "is_reply": true, "parent_comment_id": "UgzarqjaaPC7TbFINNx4AaABAg", "published_date": "2 years ago (edited)", "crawled_date": "2023-09-18T02:31:29.264043", "is_video_owner": false}
{"video_id": "dQw4w9WgXcQ", "author": "@mune1", "comment": ["If you are seeing this you probably got rickrolled ", "😔"], "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg.9QM9WCCnud69QM9YYj-kTm", "like_count": "65K", "reply_count": 0, "is_reply": true, "parent_comment_id": "UgzarqjaaPC7TbFINNx4AaABAg", "published_date": "2 years ago (edited)", "crawled_date": "2023-09-18T02:31:29.264043", "is_video_owner": false}
{"video_id": "dQw4w9WgXcQ", "author": "@aliale161", "comment": ["Rick'd"], "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg.9QM9WCCnud69QM9YghC1wE", "like_count": "38K", "reply_count": 0, "is_reply": true, "parent_comment_id": "UgzarqjaaPC7TbFINNx4AaABAg", "published_date": "2 years ago (edited)", "crawled_date": "2023-09-18T02:31:29.264043", "is_video_owner": false}
{"video_id": "dQw4w9WgXcQ", "author": "@ZerakimSC2", "comment": ["1 BILLION BABY!"], "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg.9QM9WCCnud69QM9YnKUTOD", "like_count": "34K", "reply_count": 0, "is_reply": true, "parent_comment_id": "UgzarqjaaPC7TbFINNx4AaABAg", "published_date": "2 years ago", "crawled_date": "2023-09-18T02:31:29.264043", "is_video_owner": false}
{"video_id": "dQw4w9WgXcQ", "author": "@dan_shercat", "comment": ["This video is the reason I'm afraid of clicking links."], "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg.9QM9WCCnud69QM9YrMhOkO", "like_count": "32K", "reply_count": 0, "is_reply": true, "parent_comment_id": "UgzarqjaaPC7TbFINNx4AaABAg", "published_date": "2 years ago (edited)", "crawled_date": "2023-09-18T02:31:29.264043", "is_video_owner": false}
{"video_id": "dQw4w9WgXcQ", "author": "@DVFT", "comment": ["Fun Fact:", "\n", "\n", "\n", "\n", "‎", "\n", "‎"], "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg.9QM9WCCnud69QM9Yv5lnLT", "like_count": "34K", "reply_count": 0, "is_reply": true, "parent_comment_id": "UgzarqjaaPC7TbFINNx4AaABAg", "published_date": "2 years ago (edited)", "crawled_date": "2023-09-18T02:31:29.264043", "is_video_owner": false}
{"video_id": "dQw4w9WgXcQ", "author": "@cryux3691", "comment": ["Yo"], "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg.9QM9WCCnud69QM9Z69KVBw", "like_count": "16K", "reply_count": 0, "is_reply": true, "parent_comment_id": "UgzarqjaaPC7TbFINNx4AaABAg", "published_date": "2 years ago", "crawled_date": "2023-09-18T02:31:29.264043", "is_video_owner": false}
{"video_id": "dQw4w9WgXcQ", "author": "@jrxjared1621", "comment": ["YOO BIG FAN HERE!", "\n", "\n", " congratulations Rick, you are a legend!!!"], "comment_id": "UgzarqjaaPC7TbFINNx4AaABAg.9QM9WCCnud69QM9Z9m-U5E", "like_count": "16K", "reply_count": 0, "is_reply": true, "parent_comment_id": "UgzarqjaaPC7TbFINNx4AaABAg", "published_date": "2 years ago (edited)", "crawled_date": "2023-09-18T02:31:29.264043", "is_video_owner": false}
```

---
