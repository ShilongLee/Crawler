from .common import pack_search_query, SEARCH_URL
import requests
import json
import re

def request_search(keyword: str, cookie: str, page: int = 1, page_size: int = 48) -> tuple[dict, bool]:
    """
    请求taobao获取搜索信息
    """
    ret = []
    query = pack_search_query(cookie, keyword, page, page_size)
    url = f'{SEARCH_URL}{query}'
    headers = {'cookie': cookie}  # 未使用proxies
    try:
        print(url)
        with requests.get(url, headers=headers) as res:
            res_str = re.sub(r'^\s*mtopjsonp2\(|\)$', '', res.text)
            print(res_str)
            res = json.loads(res_str)
            ret = res["data"]["itemsArray"]
    except Exception as e:
        print(e)
        return {}, False

    return ret, True
