from .common import common_request, API_HOST

def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 10) -> tuple[dict, bool]:
    """
    请求bilibili获取搜索信息
    """
    params = {"keyword": keyword, "search_type": 'video'}
    headers = {"cookie": cookie}
    page_size = 20
    start_page = int((offset - 1) / page_size )+ 1
    end_page = int((offset + limit - 1) / page_size) + 1
    ret = []
    for page in range(start_page, end_page + 1):
        params['page'] = page
        resp, succ = common_request(API_HOST, '/x/web-interface/search/type', params, headers, False, True)
        if not succ:
            return {}, succ
        ret.extend(resp.get('data', {}).get('result', []))
    ret = ret[(offset % page_size):(offset % page_size + limit)]
    return ret, True