from .common import common_request, load_graphql_queries, GraphqlQuery
import asyncio

async def request_user(id: str, cookie: str, offset: int = 0, limit: int = 20) -> dict:
    """
    请求快手获取用户信息
    """
    ret = {}
    # 获取用户信息
    tasks = [request_user_detail(id, cookie), request_user_photo(id, offset, limit, cookie)]

    results = await asyncio.gather(*tasks)
    user, photos = results[0], results[1]
    ret['user'] = user
    # 获取作品
    ret['photos'] = photos[offset:offset+limit]
    return ret

async def request_user_detail(id: str, cookie: str) -> dict:
    data = {
        "operationName": "visionProfile",
        "variables": {
            "userId": id,
        },
        "query": load_graphql_queries(GraphqlQuery.PROFILE)
    }
    headers = {"cookie": cookie}
    resp, succ = await common_request(data, headers)
    if not succ:
        return {}
    return resp.get('data', {}).get('visionProfile', {})

async def request_user_photo(id: str, offset: int, limit: int, cookie: str) -> list:
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
        resp, succ = await common_request(data, headers)
        if not succ:
            return photos
        photos.extend(resp.get('data', {}).get('visionProfilePhotoList', {}).get('feeds', []))
        pcursor = resp.get('data', {}).get('visionProfilePhotoList', {}).get('pcursor', '')
    return photos