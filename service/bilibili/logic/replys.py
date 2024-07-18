from .common import common_request, detail_request, API_HOST
from asyncio import gather

async def request_replys(id: str, comment_id: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求bilibili获取评论回复信息
    """
    headers = {"cookie": cookie}
    data, succ = await detail_request(id, headers)
    if not succ:
        return data, succ
    oid = data.get('aid', 0)

    page_size = 10
    start_page = int( offset / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    comments = []
    total = 0
    tasks = [request_page(oid, comment_id, cookie, page, page_size) for page in range(start_page, end_page + 1)]
    results = await gather(*tasks)
    for result in results:
        comments.extend(result[0])
        total = result[1] if result[1] > 0 else total

    ret = {'total': total, 'comments': comments[(offset % page_size):(offset % page_size + limit)]}
    return ret, True

async def request_page(oid: int, comment_id: str, cookie: str, page: int, page_size: int = 10) -> tuple[list, int]:
    headers = {"cookie": cookie}
    params = {"oid": oid, "type": 1, "root": comment_id, "ps": page_size, "pn": page, 'gaia_source': 'main_web', 'web_location': '333.788'}
    resp, succ = await common_request(API_HOST, '/x/v2/reply/reply', params, headers, False, True)
    if not succ:
        return {}, succ
    data = resp.get('data', {})
    return data.get('replies', []), data.get('page', {}).get('count', 0)