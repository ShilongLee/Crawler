from .common import mobile_common_request
import asyncio

async def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 10) -> dict:
    """
    请求微博获取搜索信息
    """
    results = []
    total = 0
    page_size = 10
    start_page = int( offset / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    tasks = [request_page(page, keyword, cookie) for page in range(start_page, end_page + 1)]
    pages = await asyncio.gather(*tasks)
    for data in pages:
        total = data.get('cardlistInfo', {}).get('total') if data.get('cardlistInfo', {}).get('total') else total
        results.extend(data.get('cards', []))

    ret = {'total': total, 'results': results[(offset % page_size):(offset % page_size + limit)]}
    return ret

async def request_page(page: int, keyword: str, cookie: str) -> dict:
    headers = {"Cookie": cookie}
    params = {
            'containerid': f'100103type=1&q={keyword}',
            'page_type': 'searchall',
            'page': page
        }
    resp, succ = await mobile_common_request('/api/container/getIndex', params, headers)
    if not succ:
        return {}
    return resp.get('data', {})