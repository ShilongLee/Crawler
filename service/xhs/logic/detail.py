from .common import common_request


async def request_detail(id: str, cookie: str) -> tuple[dict, bool]:
    """
    请求小红书获取视频信息
    """
    params = {"source_note_id": id, "image_formats": [
        "jpg", "webp", "avif"], "extra": {"need_body_topic": "1"}}
    headers = {"cookie": cookie}
    resp, succ = await common_request('/api/sns/web/v1/feed', params, headers)
    if not succ:
        return {}, succ
    ret = resp.get('data', {})
    return ret, succ
