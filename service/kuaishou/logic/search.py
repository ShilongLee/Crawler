from .common import common_request, load_graphql_queries, GraphqlQuery

async def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求快手获取搜索信息
    """
    pcursor = ''
    headers = {"Cookie": cookie}
    page_size = 20
    start_page = int( offset / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    ret = []
    search_session_id = None
    for page in range(start_page, end_page + 1):
        if page - 1 > 0:
            pcursor = str(page-1)
        data = {
            "operationName": "visionSearchPhoto",
            "variables": {
                "keyword": keyword,
                "pcursor": pcursor,
                "page": "search"
            },
            "query": load_graphql_queries(GraphqlQuery.SEARCH)
        }
        if search_session_id and search_session_id != '':
            data['variables']['searchSessionId'] = search_session_id
        resp, succ = await common_request(data, headers)
        if not succ:
            return {}, succ
        data = resp.get('data', {}).get('visionSearchPhoto', {}).get('feeds', [])
        search_session_id = resp.get('data', {}).get('visionSearchPhoto', {}).get('searchSessionId', '')
        ret.extend(data)
    ret = ret[(offset % page_size):(offset % page_size + limit)]
    return ret, succ
