from .common import common_request, detail_request, API_HOST
def request_replys(id: str, comment_id: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求bilibili获取评论回复信息
    """
    headers = {"cookie": cookie}
    data, succ = detail_request(id, headers)
    if not succ:
        return data, succ
    oid = data.get('aid', 0)
    page_size = 10
    start_page = int((offset - 1) / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    comments = []
    total = 0
    for page in range(start_page, end_page + 1):
        params = {"oid": oid, "type": 1, "root": comment_id, "ps": page_size, "pn": page, 'gaia_source': 'main_web', 'web_location': '333.788'}
        resp, succ = common_request(API_HOST, '/x/v2/reply/reply', params, headers, False, True)
        if not succ:
            return {}, succ
        data = resp.get('data', {})
        comments.extend(data.get('replies', []))
        total = data.get('page', {}).get('count', 0)
    
    ret = {'total': total, 'comments': comments[(offset % page_size):(offset % page_size + limit)]}
    return ret, True
