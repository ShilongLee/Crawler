from .common import common_request, load_graphql_queries, GraphqlQuery
from lib.logger import logger

def request_replys(video_id: str, comment_id: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求快手获取评论回复信息
    """
    pcursor = ''
    headers = {"cookie": cookie}
    end_length = offset + limit
    ret = []
    while pcursor != 'no_more' and len(ret) < end_length:
        data = {
            "operationName": "visionSubCommentList",
            "variables": {
                "photoId": video_id,
                "rootCommentId": comment_id,
                "pcursor": pcursor
            },
            "query": load_graphql_queries(GraphqlQuery.REPLYS)

        }
        resp, succ = common_request(data, headers)
        if not succ:
            return resp, succ
        ret.extend(resp.get('data', {}).get('visionSubCommentList', {}).get('subComments', []))
        pcursor = resp.get('data', {}).get('visionSubCommentList', {}).get('pcursor', '')
        logger.info(f'目标长度:{end_length} comments: {len(ret)}')

    ret = ret[offset:end_length]
    return ret, succ