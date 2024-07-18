from .common import common_request, API_HOST
from asyncio import gather

async def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 10) -> dict:
    """
    请求bilibili获取搜索信息
    """
    page_size = 20
    start_page = int( offset / page_size )+ 1
    end_page = int((offset + limit - 1) / page_size) + 1
    ret = []
    tasks = [request_page(keyword, cookie, page) for page in range(start_page, end_page + 1)]
    pages = await gather(*tasks)
    for page in pages:
        ret.extend(page)
    ret = ret[(offset % page_size):(offset % page_size + limit)]
    return ret

async def request_page(keyword: str, cookie: str, page: int) -> list:
    headers = {"cookie": cookie}
    params = {"keyword": keyword, "search_type": 'video', 'page': page}
    resp, succ = await common_request(API_HOST, '/x/web-interface/search/type', params, headers, False, True)
    if not succ:
        return []
    return resp.get('data', {}).get('result', [])