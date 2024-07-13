from .common import common_request, WEB_HOST
from bs4 import BeautifulSoup
from lib import requests
from lib.logger import logger
import re
import json
import asyncio

async def request_user(id: str, cookie: str, offset: int = 0, limit: int = 20) -> dict:
    """
    请求小红书获取用户信息
    """
    ret = {}
    tasks = [request_user_detail(id), request_user_notes(id, cookie, offset, limit)]
    results = await asyncio.gather(*tasks)
    user_data, notes = results[0], results[1]
    ret["user"] = user_data.get('user', {})
    ret["user"]['notes'] = notes[offset:offset + limit]
    return ret

# 获取用户信息
async def request_user_detail(id: str) -> dict:
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    response = await requests.get(f'{WEB_HOST}/user/profile/{id}', headers=headers)
    if response.status_code != 200 or response.text == '':
        logger.error(f'failed get xhs user detail，id: {id}, code：{response.status_code}， body: {response.text}')
        return {}
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile('window\\.__INITIAL_STATE__=')
    target = soup.find('script', text = pattern).text.replace('window.__INITIAL_STATE__=', '').replace('undefined', 'null')
    data = json.loads(target)
    return data

# 获取作品
async def request_user_notes(id: str, cookie: str, offset: int = 0, limit: int = 20) -> list:
    end_length = offset + limit
    notes = []
    cursor = ''
    has_more = True
    headers = {'cookie': cookie}
    while has_more and len(notes) < end_length:
        params = {"num": 30, "cursor": cursor, "user_id": id, "image_formats": ["jpg", "webp", "avif"], "id": 1}
        resp, succ = await common_request('/api/sns/web/v1/user_posted', params, headers, True, False)
        if not succ:
            return []
        notes.extend(resp.get('data', {}).get('notes', []))
        cursor = resp.get('data', {}).get('cursor', '')
        has_more = resp.get('data', {}).get('has_more', False)
    return notes