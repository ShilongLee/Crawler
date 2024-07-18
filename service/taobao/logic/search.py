from .common import pack_search_query, SEARCH_URL, COMMON_HEADERS
from lib.logger import logger
from lib import requests
import json
import re
import asyncio

async def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 48) -> dict:
    """
    请求taobao获取搜索信息
    """
    results = []
    page_size = 48
    start_page = int( offset / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    total = 0
    
    tasks = [search(keyword, cookie, page) for page in range(start_page, end_page + 1)]
    results = await asyncio.gather(*tasks)
    for data in results:
        results.extend(data.get('itemsArray', []))
        total = data.get('mainInfo', {}).get('totalResults', 0)

    ret = {'total': total, 'results': results[(offset % page_size):(offset % page_size + limit)]}
    return ret

async def search(keyword: str, cookie: str, page: int) -> dict:
    headers = {'cookie': cookie}
    headers.update(COMMON_HEADERS)
    query = pack_search_query(cookie, keyword, page)
    url = f'{SEARCH_URL}{query}'
    try:
        logger.info(f'request url: {url}')
        resp = await requests.get(url, headers=headers)
        logger.info(f'response url: {url}, body: {resp.text}')
        res_str = re.sub(r'^\s*mtopjsonp2\(|\)$', '', resp.text)
        res = json.loads(res_str)
        return res.get('data', {})
    except Exception as e:
        logger.error(f"failed to request {url}, error: {e}")
        return {}