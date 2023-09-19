import json
import sys
import urllib.error
import urllib.parse
import urllib.request
import urllib.response
from typing import MutableMapping, Union


def log_stderr(error: Union[str, Exception]):
    print(str(error) if isinstance(error, Exception) else error, file=sys.stderr)


def get(url: str, headers: MutableMapping[str, str]) -> str:
    return make_request(url=url, hdr=headers)


def post(url: str, data: MutableMapping[str, str], headers: MutableMapping[str, str]) -> str:
    return make_request(url=url, data=data, hdr=headers, method='POST')


def make_request(url, hdr: MutableMapping[str, str] = None, data: MutableMapping[str, str] = None, method: str = 'GET'):
    if data is not None:
        data_encoded = json.dumps(data).encode('utf-8')
    else:
        data_encoded = None

    req = urllib.request.Request(url, data=data_encoded, headers=hdr, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                return resp.read().decode('utf-8')
            else:
                raise urllib.error.HTTPError(url, resp.status, "Failed to retrieve", resp.headers, None)
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        log_stderr(e)
        raise e
