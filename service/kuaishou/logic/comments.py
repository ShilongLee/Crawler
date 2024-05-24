from .common import common_request, load_graphql_queries, GraphqlQuery

def request_comments(id: str, cookie: str, pcursor: str = '') -> tuple[dict, bool]:
    """
    请求快手获取评论信息
    """
    headers = {"cookie": cookie}
    data = {
        "operationName": "commentListQuery",
        "variables": {
            "photoId": id,
            "pcursor": pcursor
        },
        "query": load_graphql_queries(GraphqlQuery.COMMENTS)

    }
    return common_request(data, headers)
