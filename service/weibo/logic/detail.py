from .common import mobile_common_request
import re
import json

def request_detail(id: str) -> tuple[dict, bool]:
    """
    请求微博获取微博信息
    """
    resp, succ = mobile_common_request(f'/detail/{id}', {}, {}, True)
    if not succ:
        return resp, succ
    match = re.search(r'var \$render_data = (\[.*?\])\[0\]', resp, re.DOTALL)
    if match:
        text = match.group(1)
        data = json.loads(text)
        detail = data[0].get("status", {})
        return detail, True
    return {}, False