from .common import common_request

async def request_detail(id: str, cookie: str) -> tuple[dict, bool]:
    """
    请求抖音获取视频信息
    """
    params = {"aweme_id": id}
    headers = {"cookie": cookie}
    resp, succ = await common_request('/aweme/v1/web/aweme/detail/', params, headers)
    if not succ:
        return resp, succ
    ret = resp.get('aweme_detail', {})
    return ret, succ