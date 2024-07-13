from .common import common_request

async def request_comments(id: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求微博获取评论信息
    """
    headers = {"cookie": cookie}
    end_length = offset + limit
    comments = []
    max_id = 0
    total = 0
    is_end = False
    while not is_end and len(comments) < end_length:
        params = {
            "id": id,
            "is_show_bulletin": 2,
            "is_mix": 0,
            "count": 10,
            # "uid": 123, # 可通过profile获取，非强制参数
            "fetch_level": 0,
            "locale": "zh-CN",
            "max_id": max_id
        }
        resp, succ = await common_request('/ajax/statuses/buildComments', params, headers)
        if not succ:
            return {}, succ
        comments.extend(resp.get('data', []))
        max_id = int(resp.get('max_id', 0))
        total = resp.get('total_number', 0)
        is_end = max_id == 0 

    ret = {'total': total, 'comments': comments[offset:end_length]}
    return ret, succ
