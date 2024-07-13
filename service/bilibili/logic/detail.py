from .common import detail_request
async def request_detail(id: str, cookie: str) -> tuple[dict, bool]:
    """
    请求Bilibili获取视频信息
    """
    headers = {"cookie": cookie}
    return await detail_request(id, headers)