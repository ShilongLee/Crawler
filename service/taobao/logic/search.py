from .common import pack_search_query, SEARCH_URL, COMMON_HEADERS
import requests
import json
import re
from lib.logger import logger

def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 48) -> tuple[dict, bool]:
    """
    请求taobao获取搜索信息
    """
    results = []
    page_size = 48
    start_page = int((offset - 1) / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    headers = {'cookie': cookie}
    headers.update(COMMON_HEADERS)
    total = 0
    for page in range(start_page, end_page + 1):
        query = pack_search_query(cookie, keyword, page)
        url = f'{SEARCH_URL}{query}'
        try:
            logger.info(f'request url: {url}')
            with requests.get(url, headers=headers) as res:
                logger.info(f'response url: {url}, body: {res.text}')
                res_str = re.sub(r'^\s*mtopjsonp2\(|\)$', '', res.text)
                res = json.loads(res_str)
                results.extend(res.get('data', {}).get('itemsArray', []))
                total = res.get('data', {}).get('mainInfo', {}).get('totalResults', 0)
        except Exception as e:
            logger.error(f"failed to request {url}, error: {e}")
            return {}, False

    ret = {'total': total, 'results': results[(offset % page_size):(offset % page_size + limit)]}
    return ret, True
