from .common import common_request

async def request_comments(id: str, cookie: str, offset: int, limit: int) -> tuple[dict, bool]:
    """
    请求小红书获取评论信息
    """
    cursor = ''
    headers = {"cookie": cookie}
    end_length = offset + limit
    comments = []
    has_more = True
    while has_more and len(comments) < end_length:
        data = {
            "note_id": id,
            "cursor": cursor,
            "top_comment_id": '',
            "image_formats": ["jpg", "webp", "avif"]
        }
        resp, succ = await common_request('/api/sns/web/v2/comment/page', data, headers, True, False)
        if not succ:
            return {}, succ
        has_more = resp.get('data', {}).get('has_more', False)
        comments.extend(resp.get('data', {}).get('comments', []))
        cursor = resp.get('data', {}).get('cursor', '')

    ret = {"comments": comments[offset:end_length]}
    return ret, succ
