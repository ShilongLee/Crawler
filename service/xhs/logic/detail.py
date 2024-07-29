from .common import common_request, COMMON_HEADERS
from lib import requests
from lib import logger
import re



async def request_detail(id: str, cookie: str) -> tuple[dict, bool]:
    """
    请求小红书获取视频信息
    """
    # 获取xsec_token
    url = 'https://www.xiaohongshu.com/explore'
    headers = {"cookie": cookie}
    headers.update(COMMON_HEADERS)
    resp = await requests.get(url, headers=headers)
    if resp.status_code != 200 or resp.text == '':
        return {}, False
    pattern = r'xsec_token=(.*?)&'
    match = re.search(pattern, resp.text)
    if not match:
        logger.error("No xsec_token match found.")
        return {}, False
    xsec_token = match.group(1)

    # 获取详情
    params = {"source_note_id": id, "image_formats": [
        "jpg", "webp", "avif"], "extra": {"need_body_topic": "1"}, "xsec_source": "pc_feed", "xsec_token": xsec_token}
    headers = {"cookie": cookie}
    resp, succ = await common_request('/api/sns/web/v1/feed', params, headers)
    if not succ:
        return {}, succ
    ret = resp.get('data', {})
    return ret, succ
