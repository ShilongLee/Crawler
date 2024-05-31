from .common import detail_request
def request_detail(id: str, cookie: str) -> tuple[dict, bool]:
    """
    请求Bilibili获取视频信息
    """
    headers = {"cookie": cookie}
    return detail_request(id, headers)