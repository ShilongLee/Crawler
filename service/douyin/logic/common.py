import execjs
import requests
import urllib.parse
from lib.logger import logger

HOST = 'https://www.douyin.com'

COMMON_PARAMS = {
    "device_platform": "webapp",
    "aid": "6383",
    "channel": "channel_pc_web",
    "cookie_enabled": "true",
    "browser_language": "zh-CN",
    "browser_platform": "Win32",
    "browser_name": "Firefox",
    "browser_version": "110.0",
    "browser_online": "true",
    "engine_name": "Gecko",
    "os_name": "Windows",
    "os_version": "10",
    "engine_version": "109.0",
    "platform": "PC",
    "screen_width": "1920",
    "screen_height": "1200",
}

COMMON_HEADERS ={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "sec-fetch-site": "same-origin",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "sec-ch-ua-platform": "macOS",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "referer": "https://www.douyin.com/?recommend=1",
    "priority": "u=1, i",
    "pragma": "no-cache",
    "cache-control": "no-cache",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "accept": "application/json, text/plain, */*",
    "dnt": "1",
}

def common_request(uri: str, params: dict, headers: dict) -> tuple[dict, bool]:
    url = f'{HOST}{uri}'
    params.update(COMMON_PARAMS)
    headers.update(COMMON_HEADERS)

    douyin_sign_obj = execjs.compile(open('lib/js/douyin.js').read())
    query = '&'.join([f'{k}={urllib.parse.quote(str(v))}' for k, v in params.items()])
    x_bogus = douyin_sign_obj.call('sign', query, headers["User-Agent"])
    params["X-Bogus"] = x_bogus

    logger.info(
        f'url: {url}, request {url}, params={params}, headers={headers}')
    response = requests.get(url, params=params, headers=headers)
    logger.info(
        f'url: {url}, params: {params}, response, code: {response.status_code}, body: {response.text}')

    if response.status_code != 200 or response.text == '':
        logger.error(
            f'url: {url}, params: {params}, request error, code: {response.status_code}, body: {response.text}')
        return {}, False
    if response.json().get('status_code', 0) != 0:
        logger.error(
            f'url: {url}, params: {params}, request error, code: {response.status_code}, body: {response.text}')
        return response.json(), True

    return response.json(), False