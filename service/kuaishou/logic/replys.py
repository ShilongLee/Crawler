from .common import common_request, load_graphql_queries, GraphqlQuery

async def request_replys(id: str, comment_id: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求快手获取评论回复信息
    """
    pcursor = ''
    headers = {"cookie": cookie}
    end_length = offset + limit
    comments = []
    while pcursor != 'no_more' and len(comments) < end_length:
        data = {
            "operationName": "visionSubCommentList",
            "variables": {
                "photoId": id,
                "rootCommentId": comment_id,
                "pcursor": pcursor
            },
            "query": load_graphql_queries(GraphqlQuery.REPLYS)

        }
        resp, succ = await common_request(data, headers)
        if not succ:
            return {}, succ
        comments.extend(resp.get('data', {}).get('visionSubCommentList', {}).get('subComments', []))
        pcursor = resp.get('data', {}).get('visionSubCommentList', {}).get('pcursor', '')

    ret = {"comments": comments[offset:end_length]}
    
    return ret, succ