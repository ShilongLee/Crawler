from .common import common_request

def request_user(id: str, cookie: str, offset: int = 0, limit: int = 20) -> tuple[dict, bool]:
    """
    请求抖音获取用户信息
    """
    ret = {}
    # 获取用户信息
    params = {"publish_video_strategy_type": 2,
              "sec_user_id": id, "personal_center_strategy": 1}
    headers = {"cookie": cookie}
    resp, succ = common_request(
        '/aweme/v1/web/user/profile/other/', params, headers)
    if not succ:
        return ret, succ
    ret['user'] = resp.get('user', {})

    # 获取作品
    end_length = offset + limit
    videos = []
    max_cursor = 0
    has_more = True
    while has_more and len(videos) < end_length:
        params = {"publish_video_strategy_type": 2, "max_cursor": max_cursor, "locate_query": False,
              'show_live_replay_strategy': 1, 'need_time_list': 0, 'time_list_query': 0, 'whale_cut_token': '', 'count': 18, "sec_user_id": id}
        resp, succ = common_request('/aweme/v1/web/aweme/post/', params, headers)
        if not succ:
            return resp, succ
        videos.extend(resp.get('aweme_list', []))
        max_cursor = resp.get('max_cursor', 0)
        has_more = resp.get('has_more', 0) == 1
    ret['aweme_list'] = videos[offset:end_length]
    return ret, succ
