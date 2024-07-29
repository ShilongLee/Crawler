from lib.logger import logger
import execjs
from lib import requests
import urllib.parse
import re
import random

HOST = 'https://www.douyin.com'

COMMON_PARAMS = {
    'device_platform': 'webapp',
    'aid': '6383',
    'channel': 'channel_pc_web',
    'update_version_code': '170400',
    'pc_client_type': '1', # Windows
    'version_code': '190500',
    'version_name': '19.5.0',
    'cookie_enabled': 'true',
    'screen_width': '2560', # from cookie dy_swidth
    'screen_height': '1440', # from cookie dy_sheight
    'browser_language': 'zh-CN',
    'browser_platform': 'Win32',
    'browser_name': 'Chrome',
    'browser_version': '126.0.0.0',
    'browser_online': 'true',
    'engine_name': 'Blink',
    'engine_version': '126.0.0.0',
    'os_name': 'Windows',
    'os_version': '10',
    'cpu_core_num': '24',   # device_web_cpu_core
    'device_memory': '8',   # device_web_memory_size
    'platform': 'PC',
    'downlink': '10',
    'effective_type': '4g',
    'round_trip_time': '50',
    # 'webid': '7378325321550546458',   # from doc
    # 'verifyFp': 'verify_lx6xgiix_cde2e4d7_7a43_e749_7cda_b5e7c149c780',   # from cookie s_v_web_id
    # 'fp': 'verify_lx6xgiix_cde2e4d7_7a43_e749_7cda_b5e7c149c780', # from cookie s_v_web_id
    # 'msToken': 'hfAykirauBE-RKDm8bF2o2_cKuSdwHsbGXjJBuo8s3w9n46-Tu0CtxX7-iiZWZ8D7mRUAmRAkeiaU35194AJehc9u6_mei3Q9s_LABQuoANQmbd81DDS3wuA5u9UVIo%3D',  # from cookie msToken
    # 'a_bogus': 'xJRwQfLfDkdsgDyh54OLfY3q66M3YQnV0trEMD2f5V3WF639HMPh9exLx-TvU6DjNs%2FDIeEjy4haT3nprQVH8qw39W4x%2F2CgQ6h0t-P2so0j53iJCLgmE0hE4vj3SlF85XNAiOk0y7ICKY00AInymhK4bfebY7Y6i6tryE%3D%3D' # sign
}

COMMON_HEADERS ={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "sec-ch-ua-platform": "Windows",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
    "referer": "https://www.douyin.com/?recommend=1",
    "priority": "u=1, i",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "accept": "application/json, text/plain, */*",
    "dnt": "1",
}

DOUYIN_SIGN = execjs.compile(open('lib/js/douyin.js', encoding='utf-8').read())

async def get_webid(headers: dict):
    url = 'https://www.douyin.com/?recommend=1'
    logger.info(
        f'url: {url}, request {url}, headers={headers}')
    headers['sec-fetch-dest'] = 'document'
    response = await requests.get(url, headers=headers)
    logger.info(
        f'url: {url}, response, code: {response.status_code}')
    if response.status_code != 200 or response.text == '':
        logger.error(f'failed get webid, url: {url}, header: {headers}')
        return None
    pattern = r'\\"user_unique_id\\":\\"(\d+)\\"'
    match = re.search(pattern, response.text)
    if match:
        return match.group(1)
    return None

def cookies_to_dict(cookie_string) -> dict:
    cookies = cookie_string.split('; ')
    cookie_dict = {}
    for cookie in cookies:
        if cookie == '' or cookie == 'douyin.com':
            continue
        key, value = cookie.split('=', 1)[0],  cookie.split('=', 1)[1]
        cookie_dict[key] = value
    return cookie_dict

async def deal_params(params: dict, headers: dict) -> dict:
    cookie = headers.get('cookie') or headers.get('Cookie')
    if not cookie:
        return params
    cookie_dict = cookies_to_dict(cookie)
    params['msToken'] = get_ms_token()
    params['screen_width'] = cookie_dict.get('dy_swidth', 2560)
    params['screen_height'] = cookie_dict.get('dy_sheight', 1440)
    params['cpu_core_num'] = cookie_dict.get('device_web_cpu_core', 24)
    params['device_memory'] = cookie_dict.get('device_web_memory_size', 8)
    params['verifyFp'] = cookie_dict.get('s_v_web_id', None)
    params['fp'] = cookie_dict.get('s_v_web_id', None)
    params['webid'] = await get_webid(headers)
    return params

def get_ms_token(randomlength=120):
    """
    根据传入长度产生随机字符串
    """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789='
    length = len(base_str) - 1
    for _ in range(randomlength):
        random_str += base_str[random.randint(0, length)]
    return random_str

async def common_request(uri: str, params: dict, headers: dict) -> tuple[dict, bool]:
    """
    请求 douyin
    :param uri: 请求路径
    :param params: 请求参数
    :param headers: 请求头
    :return: 返回数据和是否成功
    """
    url = f'{HOST}{uri}'
    params.update(COMMON_PARAMS)
    headers.update(COMMON_HEADERS)

    params = await deal_params(params, headers)
    query = '&'.join([f'{k}={urllib.parse.quote(str(v))}' for k, v in params.items()])
    call_name = 'sign_datail'
    if 'reply' in uri:
        call_name = 'sign_reply'
    a_bogus = DOUYIN_SIGN.call(call_name, query, headers["User-Agent"])
    params["a_bogus"] = a_bogus

    logger.info(
        f'url: {url}, request {url}, params={params}, headers={headers}')
    response = await requests.get(url, params=params, headers=headers)
    logger.info(
        f'url: {url}, params: {params}, response, code: {response.status_code}, body: {response.text}')

    if response.status_code != 200 or response.text == '':
        logger.error(
            f'url: {url}, params: {params}, request error, code: {response.status_code}, body: {response.text}')
        return {}, False
    if response.json().get('status_code', 0) != 0:
        logger.error(
            f'url: {url}, params: {params}, request error, code: {response.status_code}, body: {response.text}')
        return response.json(), False

    return response.json(), True