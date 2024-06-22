from .common import common_request, get_dm_img, API_HOST

def request_user(id: str, cookie: str, offset: int = 0, limit: int = 30) -> tuple[dict, bool]:
    """
    请求Bilibili获取用户信息
    """
    # 获取用户信息
    ret = {}
    headers = {'cookie': cookie}
    params = {
        "mid": id,
        "token": "",
        "platform": "web",
        "web_location": 1550101
    }
    params.update(get_dm_img(False))
    resp, succ = common_request(
        API_HOST, '/x/space/wbi/acc/info', params, headers, False, True)
    if not succ:
        return resp, succ
    ret.update(resp.get('data', {}))

    # 获取粉丝数
    params = {
        "vmid": id,
        "web_location": "333.999",
    }
    resp, succ = common_request(
        API_HOST, '/x/relation/stat', params, headers, False, True)
    if not succ:
        return resp, succ
    ret.update(resp.get('data', {}))

    # 获取点赞数
    params = {
        "mid": id,
        "web_location": "333.999",
    }
    resp, succ = common_request(
        API_HOST, '/x/space/upstat', params, headers, False, False)
    if not succ:
        return resp, succ
    ret.update(resp.get('data', {}))

    # 获取作品
    page_size = 30
    start_page = int((offset - 1) / page_size) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    videos = []
    total = 0
    for page in range(start_page, end_page + 1):
        params = {"mid": id, "pn": page, "ps": page_size, "tid": 0, "keyword": "",
                  "order": "pubdate", 'platform': 'web', 'web_location': '1550101', "order_avoided": True}
        params.update(get_dm_img(True))
        resp, succ = common_request(
            API_HOST, '/x/space/wbi/arc/search', params, headers, False, True)
        if not succ:
            return {}, succ
        data = resp.get('data', {})
        videos.extend(data.get('list', {}).get("vlist", []))
        total = data.get('page', {}).get('count', 0)
    videos = videos[(offset % page_size):(offset % page_size + limit)]
    ret["videos"] = {
        "list": videos,
        "total": total,
    }
    return ret, True
