from .common import pack_search_query, SEARCH_URL, COMMON_HEADERS
import requests
import json
import re
from lib.logger import logger

def request_search(keyword: str, cookie: str, page: int = 1) -> tuple[dict, bool]:
    """
    请求taobao获取搜索信息
    """
    ret = []
    query = pack_search_query(cookie, keyword, page)
    url = f'{SEARCH_URL}{query}'
    headers = {'cookie': cookie}
    headers.update(COMMON_HEADERS)
    try:
        logger.info(f'url: {url}')
        with requests.get(url, headers=headers) as res:
            res_str = re.sub(r'^\s*mtopjsonp2\(|\)$', '', res.text)
            res = json.loads(res_str)
            ret = res["data"]["itemsArray"]
            ret_count = len(ret)
            logger.info(f'ret_count: {ret_count}')
    except Exception as e:
        print(e)
        return {}, False

    return ret, True
