from .common import common_request, load_graphql_queries, GraphqlQuery

async def request_comments(id: str, cookie: str, offset: int, limit: int) -> tuple[dict, bool]:
    """
    请求快手获取评论信息
    """
    pcursor = ''
    headers = {"cookie": cookie}
    end_length = offset + limit
    comments = []
    total = 0
    while pcursor != 'no_more' and len(comments) < end_length:
        data = {
            "operationName": "commentListQuery",
            "variables": {
                "photoId": id,
                "pcursor": pcursor
            },
            "query": load_graphql_queries(GraphqlQuery.COMMENTS)

        }
        resp, succ = await common_request(data, headers)
        if not succ:
            return resp, succ
        comments.extend(resp.get('data', {}).get('visionCommentList', {}).get('rootComments', []))
        pcursor = resp.get('data', {}).get('visionCommentList', {}).get('pcursor', '')
        total = resp.get('data', {}).get('visionCommentList', {}).get('commentCount', 0)

    ret = {"total": total, "comments": comments[offset:end_length]}
    return ret, succ
