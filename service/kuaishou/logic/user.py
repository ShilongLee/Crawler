from .common import common_request, load_graphql_queries, GraphqlQuery

def request_user(id: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求抖音获取用户信息
    """
    ret = {}
    # 获取用户信息
    data = {
        "operationName": "visionProfile",
        "variables": {
            "userId": id,
        },
        "query": load_graphql_queries(GraphqlQuery.PROFILE)
    }
    headers = {"cookie": cookie}
    resp, succ = common_request(data, headers)
    if not succ:
        return ret, succ
    ret['user'] = resp.get('data', {}).get('visionProfile', {})

    # 获取作品
    pcursor = ''
    headers = {"cookie": cookie}
    end_length = offset + limit
    photos = []
    while pcursor != 'no_more' and len(photos) < end_length:
        data = {
            "operationName": "visionProfilePhotoList",
            "variables": {
                "page": "profile",
                "userId": id,
                "pcursor": pcursor
            },
            "query": load_graphql_queries(GraphqlQuery.PROFILE_PHOTO)

        }
        resp, succ = common_request(data, headers)
        if not succ:
            return ret, succ
        photos.extend(resp.get('data', {}).get('visionProfilePhotoList', {}).get('feeds', []))
        pcursor = resp.get('data', {}).get('visionProfilePhotoList', {}).get('pcursor', '')

    ret['photos'] = photos[offset:end_length]
    return ret, succ
