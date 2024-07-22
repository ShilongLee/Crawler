from .common import COMMON_HEADERS, APPKEY, HOST, get_token, sign
from lib.logger import logger
from lib import requests
from urllib.parse import quote
import time
import asyncio

async def request_comments(id: str, cookie: str, offset: int = 0 , limit: int = 20) -> dict:
    """
    请求taobao获取商品评论
    """
    page_size = 20
    start_page = int( offset / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    tasks = [request_page(id, cookie, page) for page in range(start_page, end_page + 1)]
    results = await asyncio.gather(*tasks)
    comments = []
    total = 0
    for comment_list, _total in results:
        comments.extend(comment_list)
        total = _total if _total > 0 else total

    return {'comments': comments[(offset % page_size):(offset % page_size + limit)], 'total': total}

async def request_page(id: str, cookie: str, page: int) -> tuple[list, int]:
    str_data = f'{{"itemId":"{id}","bizCode":"ali.china.tmall","channel":"pc_detail","pageSize":20,"pageNum":{page}}}'
    quote_data = quote(str_data, 'utf-8')
    token = get_token(cookie)
    timestamp = str(time.time()).replace('.', '')[0:13]
    sgn = sign(token, timestamp, APPKEY, str_data)
    param = {
        'jsv': '2.6.1',
        'appKey': APPKEY,
        't': timestamp,
        'sign': sgn,
        'api': 'mtop.alibaba.review.list.for.new.pc.detail',
        'v': '1.0',
        'isSec': '0',
        'ecode': '0',
        'timeout': '20000',
        'ttid': '2022@taobao_litepc_9.17.0',
        'AntiFlood': 'true',
        'AntiCreep': 'true',
        'dataType': 'json',
        'valueType': 'string',
        'preventFallback': 'true',
        'type': 'json',
        'data': quote_data
    }
    headers = {'cookie': cookie}
    headers.update(COMMON_HEADERS)
    url = f'{HOST}/h5/mtop.alibaba.review.list.for.new.pc.detail/1.0/'
    logger.info(f'请求商品评论, url: {url}, params: {param}')
    resp = await requests.get(url, headers=headers, params=param)
    logger.info(f'请求商品评论, code: {resp.status_code}, body: {resp.json()}, url: {url}, params: {param}')
    if resp.status_code != 200:
        logger.error(f'请求商品详情失败, status_code: {resp.status_code}')
        return [], 0
    data = resp.json().get('data', {}).get('module', {})
    return data.get('reviewVOList', []), int(data.get('foldFlagCount', 0))