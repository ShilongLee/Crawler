from .common import common_request, get_dm_img, API_HOST
from asyncio import gather

async def request_user(id: str, cookie: str, offset: int = 0, limit: int = 30) -> dict:
    """
    请求Bilibili获取用户信息
    """
    ret = {}
    page_size = 30
    start_page = int( offset / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    videos = []
    total = 0
    tasks = [request_user_detail(id, cookie), request_user_fans(id, cookie), request_user_likes(id, cookie)]
    tasks.extend([request_page(id, cookie, page, page_size) for page in range(start_page, end_page + 1)])
    results = await gather(*tasks)
    detail_result, fans_result, like_result, videos_result = results[0], results[1], results[2], results[3:]
    ret.update(detail_result)
    ret.update(fans_result)
    ret.update(like_result)
    for _videos, count in videos_result:
        videos.extend(_videos)
        total = count if count > 0 else total

    ret["videos"] = {
        "list": videos,
        "total": total,
    }
    return ret

async def request_user_detail(id: str, cookie) -> dict:
    headers = {'cookie': cookie}
    params = {
        "mid": id,
        "token": "",
        "platform": "web",
        "web_location": 1550101
    }
    params.update(get_dm_img(False))
    resp, succ = await common_request(
        API_HOST, '/x/space/wbi/acc/info', params, headers, False, True)
    if not succ:
        return {}
    return resp.get('data', {})

async def request_user_fans(id: str, cookie) -> dict:
    headers = {'cookie': cookie}
    params = {
        "vmid": id,
        "web_location": "333.999",
    }
    resp, succ = await common_request(
        API_HOST, '/x/relation/stat', params, headers, False, True)
    if not succ:
        return {}
    return resp.get('data', {})

async def request_user_likes(id: str, cookie) -> dict:
    headers = {'cookie': cookie}
    params = {
        "mid": id,
        "web_location": "333.999",
    }
    resp, succ = await common_request(
        API_HOST, '/x/space/upstat', params, headers, False, False)
    if not succ:
        return {}
    return resp.get('data', {})

async def request_page(id: str, cookie, page: int, page_size: int ) -> tuple[dict, int]:
    headers = {'cookie': cookie}
    params = {"mid": id, "pn": page, "ps": page_size, "tid": 0, "keyword": "",
                "order": "pubdate", 'platform': 'web', 'web_location': '1550101', "order_avoided": True}
    params.update(get_dm_img(True))
    resp, succ = await common_request(
        API_HOST, '/x/space/wbi/arc/search', params, headers, False, True)
    if not succ:
        return [], 0
    data = resp.get('data', {})
    return data.get('list', {}).get("vlist", []), data.get('page', {}).get('count', 0)
