from .common import common_request

def request_user(id: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求微博获取用户信息
    """
    ret = {}
    # 获取用户信息
    params = {"uid": id}
    headers = {"cookie": cookie}
    resp, succ = common_request('/ajax/profile/info', params, headers)
    if not succ:
        return ret, succ
    ret['user'] = resp.get('data', {}).get('user', {})

    # 获取作品
    page_size = 5
    start_page = int((offset - 1) / page_size) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    weibos = []
    total = 0
    for page in range(start_page, end_page + 1):
        params = {"uid": id, "page": page, "feature": 0}
        resp, succ = common_request('/ajax/statuses/mymblog', params, headers)
        if not succ:
            return {}, succ
        data = resp.get('data', {})
        weibos.extend(data.get('list', []))
        total = data.get('count', 0)
    weibos = weibos[(offset % page_size):(offset % page_size + limit)]
    ret["weibo"] = {
        "list": weibos,
        "total": total,
    }
    return ret, succ
