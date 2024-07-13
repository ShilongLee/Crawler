from .common import common_request
from asyncio import gather

async def request_user(id: str, cookie: str, offset: int = 0, limit: int = 10) -> dict:
    """
    请求抖音获取用户信息
    """
    tasks = [request_user_detail(id, cookie), request_user_videos(id, cookie, offset, limit)]
    results = await gather(*tasks)

    ret = {'user': results[0], 'aweme_list': results[1][offset:offset + limit]}
    return ret

async def request_user_detail(id: str, cookie: str) -> dict:
    """
    请求抖音获取用户信息
    """
    params = {"publish_video_strategy_type": 2,
              "sec_user_id": id, "personal_center_strategy": 1}
    headers = {"cookie": cookie}
    resp, succ = await common_request(
        '/aweme/v1/web/user/profile/other/', params, headers)
    if not succ:
        return {}
    return resp.get('user', {})

async def request_user_videos(id: str, cookie: str, offset: int = 0, limit: int = 10) -> list:
    """
    请求抖音获取用户视频
    """
    end_length = offset + limit
    videos = []
    max_cursor = 0
    has_more = True
    headers = {"cookie": cookie}
    while has_more and len(videos) < end_length:
        params = {"publish_video_strategy_type": 2, "max_cursor": max_cursor, "locate_query": False,
              'show_live_replay_strategy': 1, 'need_time_list': 0, 'time_list_query': 0, 'whale_cut_token': '', 'count': 18, "sec_user_id": id}
        resp, succ = await common_request('/aweme/v1/web/aweme/post/', params, headers)
        if not succ:
            return videos
        videos.extend(resp.get('aweme_list', []))
        max_cursor = resp.get('max_cursor', 0)
        has_more = resp.get('has_more', 0) == 1
    return videos