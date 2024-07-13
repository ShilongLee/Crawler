from .common import common_request
import asyncio

async def request_user(id: str, cookie: str, offset: int = 0, limit: int = 5) -> dict:
    """
    请求微博获取用户信息
    """
    ret = {}
    page_size = 5
    start_page = int((offset - 1) / page_size) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    weibos = []
    total = 0

    tasks = [reqeust_user_detail(id, cookie)]
    for page in range(start_page, end_page + 1):
        tasks.append(request_user_weibo(id, page, cookie))
    results = await asyncio.gather(*tasks)
    detail_result, weibo_result = results[0], results[1:]

    ret['user'] = detail_result

    for data in weibo_result:
        weibos.extend(data.get('list', []))
        total = data.get('count') if data.get('count') else total
    weibos = weibos[(offset % page_size):(offset % page_size + limit)]

    ret["weibo"] = {
        "list": weibos,
        "total": total,
    }
    return ret

# 获取用户信息
async def reqeust_user_detail(id: str, cookie: str) -> dict:
    params = {"uid": id}
    headers = {"cookie": cookie}
    resp, succ = await common_request('/ajax/profile/info', params, headers)
    if not succ:
        return {}
    return resp.get('data', {}).get('user', {})

# 获取用户微博
async def request_user_weibo(id: str, page: int, cookie: str) -> dict:
    headers = {"cookie": cookie}
    params = {"uid": id, "page": page, "feature": 0}
    resp, succ = await common_request('/ajax/statuses/mymblog', params, headers)
    if not succ:
        return {}
    return resp.get('data', {})