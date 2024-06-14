from .common import mobile_common_request

def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 10) -> tuple[dict, bool]:
    """
    请求微博获取搜索信息
    """
    headers = {"Cookie": cookie}
    end_length = offset + limit
    results = []
    page = 0
    total = 0
    is_end = False
    while not is_end and len(results) < end_length:
        params = {
            'containerid': f'100103type=1&q={keyword}',
            'page_type': 'searchall',
            'page': page
        }
        resp, succ = mobile_common_request('/api/container/getIndex', params, headers)
        if not succ:
            return resp, succ
        results.extend(resp.get('data', {}).get('cards', []))
        page = resp.get('data', {}).get('cardlistInfo', {}).get('page')
        total = resp.get('data', {}).get('cardlistInfo', {}).get('total', 0)
        is_end = (page == None)

    ret = {'total': total, 'results': results[offset:end_length]}
    return ret, succ
