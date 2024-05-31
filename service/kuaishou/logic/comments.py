from .common import common_request, load_graphql_queries, GraphqlQuery

def request_comments(id: str, cookie: str, offset: int, limit: int) -> tuple[dict, bool]:
    """
    请求快手获取评论信息
    """
    pcursor = ''
    headers = {"cookie": cookie}
    end_length = offset + limit
    ret = []
    while pcursor != 'no_more' and len(ret) < end_length:
        data = {
            "operationName": "commentListQuery",
            "variables": {
                "photoId": id,
                "pcursor": pcursor
            },
            "query": load_graphql_queries(GraphqlQuery.COMMENTS)

        }
        resp, succ = common_request(data, headers)
        if not succ:
            return resp, succ
        ret.extend(resp.get('data', {}).get('visionCommentList', {}).get('rootComments', []))
        pcursor = resp.get('data', {}).get('visionCommentList', {}).get('pcursor', '')

    ret = ret[offset:end_length]
    return ret, succ
