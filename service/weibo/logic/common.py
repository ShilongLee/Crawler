from lib.logger import logger
from lib import requests

HOST = 'https://weibo.com'
MOBILE_HOST = 'https://m.weibo.cn'

COMMON_PARAMS = {}
MOBILE_COMMON_PARAMS = {}

COMMON_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "client-version": "v2.45.41",
    "dnt": "1",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://weibo.com",
    "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "server-version": "v2024.06.11.3",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}
MOBILE_COMMON_HEADERS ={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "DNT": "1",
    "Pragma": "no-cache",
    "Priority": "u=0, i",
    "Referer": "https://weibo.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
}

async def mobile_common_request(uri: str, params: dict, headers: dict, doc: bool = False) -> tuple[dict, bool]:
    """
    请求 douyin
    :param uri: 请求路径
    :param params: 请求参数
    :param headers: 请求头
    :param doc: 是否返回html
    :return: 返回数据和是否成功
    """
    url = f'{MOBILE_HOST}{uri}'
    params.update(MOBILE_COMMON_PARAMS)
    headers.update(MOBILE_COMMON_HEADERS)
    
    logger.info(
        f'url: {url}, request {url}, params={params}, headers={headers}')
    response = await requests.get(url, params=params, headers=headers)
    logger.info(
        f'url: {url}, params: {params}, response, code: {response.status_code}, body: {response.text}')

    if response.status_code != 200 or response.text == '':
        logger.error(
            f'url: {url}, params: {params}, request error, code: {response.status_code}, body: {response.text}')
        return '', False
    
    if doc:
        return response.text, response.text != ''

    if response.json().get('ok', 0) != 1:
        logger.error(
            f'url: {url}, params: {params}, request error, code: {response.status_code}, body: {response.text}')
        return response.json(), False

    return response.json(), True

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
    
    logger.info(
        f'url: {url}, request {url}, params={params}, headers={headers}')
    response = await requests.get(url, params=params, headers=headers)
    logger.info(
        f'url: {url}, params: {params}, response, code: {response.status_code}, body: {response.text}')

    if response.status_code != 200 or response.text == '':
        logger.error(
            f'url: {url}, params: {params}, request error, code: {response.status_code}, body: {response.text}')
        return '', False

    if response.json().get('ok', 0) != 1:
        logger.error(
            f'url: {url}, params: {params}, request error, code: {response.status_code}, body: {response.text}')
        return response.json(), False

    return response.json(), True