from .common import common_request

def request_comments(id: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求抖音获取评论信息
    """
    headers = {"cookie": cookie}
    params = {"aweme_id": id, "cursor": offset, "count": limit, "item_type": 0}
    return common_request('/aweme/v1/web/comment/list/', params, headers)
