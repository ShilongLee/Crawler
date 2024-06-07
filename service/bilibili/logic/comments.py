from .common import common_request, detail_request, API_HOST
import json

def request_comments(id: str, cookie: str, offset: int, limit: int) -> tuple[dict, bool]:
    """
    请求bilibili获取评论信息
    """
    headers = {"cookie": cookie}
    data , succ = detail_request(id, headers)
    if not succ:
        return data, succ
    oid = data.get('aid', 0)
    end_length = offset + limit
    ret = []
    pagination = '{"offset":""}'
    is_end = False
    # tip: web_location 可能需要定期更换
    while not is_end and len(ret) < end_length:
        params = {'oid': oid, 'type': 1, 'mode': 3, 'pagination_str': pagination, 'plat': 1, 'web_location': 1315875}
        if ret == []: # 第一次要加这个参数
            params['seek_rpid'] = ''
        resp, succ = common_request(API_HOST, '/x/v2/reply/wbi/main', params, headers, False, True)
        if not succ:
            return resp, succ
        ret.extend(resp.get('data', {}).get('replies', []))
        next_offset = json.dumps(resp.get('data', {}).get('cursor', {}).get('pagination_reply', {}).get('next_offset', ''))
        pagination = '{"offset":%s}' % next_offset
        is_end = resp.get('data', {}).get('cursor', {}).get('is_end', False)
    ret = ret[offset:end_length]
    return ret, succ

