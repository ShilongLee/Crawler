from .common import common_request
async def request_replys(id: str, comment_id: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求小红书获取评论回复信息
    """
    headers = {"cookie": cookie}
    end_length = offset + limit
    comments = []
    has_more = True
    cursor = ''
    while has_more and len(comments) < end_length:
        data = {
            "note_id": id,
            "root_comment_id": comment_id,
            "num": 10,
            "cursor": cursor,
            "image_formats": ["jpg", "webp", "avif"],
            "top_comment_id": ''
        }
        resp, succ = await common_request('/api/sns/web/v2/comment/sub/page', data, headers, True, False)
        if not succ:
            return {}, succ
        has_more = resp.get('data', {}).get('has_more', False)
        comments.extend(resp.get('data', {}).get('comments', []))
        cursor = resp.get('data', {}).get('cursor', '')

    ret = {"comments": comments[offset:end_length]}
    return ret, succ
