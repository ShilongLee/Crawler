from .common import common_request
import asyncio

async def request_user(id: str, cookie: str, offset: int = 0, limit: int = 5) -> dict:
    """
    请求微博获取用户信息
    """
    ret = {}

    tasks = [reqeust_user_detail(id, cookie)]
    detail_result = await asyncio.gather(*tasks)

    ret['user'] = detail_result
    
    weibos, total = await request_user_weibo(id, cookie, offset, limit)

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
async def request_user_weibo(id: str, cookie: str, offset: int, limit: int) -> tuple[list, int]:
    headers = {"cookie": cookie}
    weibos = []
    since_id = None
    page = 1
    total = 0
    end_length = offset + limit
    while (not since_id or since_id != "") and len(weibos) < end_length:
        params = {"uid": id, "page": page, "feature": 0}
        resp, succ = await common_request('/ajax/statuses/mymblog', params, headers)
        if not succ:
            return [], 0
        weibos.extend(resp.get('data', {}).get('list', []))
        total = resp.get('data', {}).get('total', 0)
        page += 1
        since_id = resp.get('data', {}).get('since_id', "")
        
    return weibos[offset:end_length], total