from .common import common_request, load_graphql_queries, GraphqlQuery


def request_search(keyword: str, cookie: str, pcursor: str = '') -> tuple[dict, bool]:
    """
    请求快手获取搜索信息
    """
    data = {
        "operationName": "visionSearchPhoto",
        "variables": {
            "keyword": keyword,
            "pcursor": pcursor,
            "page": "search"
        },
        "query": load_graphql_queries(GraphqlQuery.SEARCH)
    }
    headers = {"Cookie": cookie}
    return common_request(data, headers)
