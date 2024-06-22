from .common import common_request, WEB_HOST
from bs4 import BeautifulSoup
import requests
import re
import json

def request_user(id: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求小红书获取用户信息
    """
    # 从doc中获取用户信息
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    response = requests.get(f'{WEB_HOST}/user/profile/{id}', headers=headers)
    if response.status_code != 200 or response.text == '':
        return {}, False
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile('window\\.__INITIAL_STATE__=')
    target = soup.find('script', text = pattern).text.replace('window.__INITIAL_STATE__=', '').replace('undefined', 'null')
    data = json.loads(target)
    ret = {"user": data.get('user', {})}

    # 获取作品
    end_length = offset + limit
    notes = []
    cursor = ''
    has_more = True
    headers = {'cookie': cookie}
    while has_more and len(notes) < end_length:
        params = {"num": 30, "cursor": cursor, "user_id": id, "image_formats": ["jpg", "webp", "avif"], "id": 1}
        resp, succ = common_request('/api/sns/web/v1/user_posted', params, headers, True, False)
        if not succ:
            return resp, succ
        notes.extend(resp.get('data', {}).get('notes', []))
        cursor = resp.get('data', {}).get('cursor', '')
        has_more = resp.get('data', {}).get('has_more', False)

    ret["user"]['notes'] = notes[offset:end_length]
    return ret, True
