from .common import common_request
import execjs


def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 10) -> tuple[dict, bool]:
    """
    请求小红书获取搜索信息
    """
    page_size = 20
    start_page = int((offset - 1) / page_size) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    headers = {"cookie": cookie}
    results = []
    xhs_sign_obj = execjs.compile(open('lib/js/xhs.js').read())
    for page in range(start_page, end_page + 1):
        params = {
            "ext_flags": [],
            "image_formats": ["jpg", "webp", "avif"],
            "keyword": keyword,
            "note_type": 0,
            "sort": "general",
            "page": page,
            "page_size": page_size,
            'search_id': xhs_sign_obj.call('searchId')
        }
        resp, succ = common_request('/api/sns/web/v1/search/notes', params, headers, True, True)
        if not succ:
            return {}, succ
        results.extend(resp.get('data', {}).get('items', []))
        if not resp.get('data', {}).get('has_more', False):
            break
    results = results[(offset % page_size):(offset % page_size + limit)]
    return results, True
