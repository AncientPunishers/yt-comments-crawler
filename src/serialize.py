from dataclasses import asdict
from datetime import datetime
from json import JSONEncoder
from typing import Any

from src import Video
from src.comment import Comment, comment_output_blacklist


def json_serial(obj: Any):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, str):
        return str.encode('utf-8')
    elif isinstance(obj, Video):
        return obj.asdict()
    elif isinstance(obj, Comment):
        return {k: v for k, v in asdict(obj).items() if k not in comment_output_blacklist}


PrettyJsonEncoder = JSONEncoder(
    indent=4,
    sort_keys=True,
    default=json_serial,
    ensure_ascii=False,
)

DefaultExportJsonEncoder = JSONEncoder(
    sort_keys=True,
    default=json_serial,
    ensure_ascii=False,
)
