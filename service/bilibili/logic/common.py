from lib.logger import logger
from bs4 import BeautifulSoup
import requests
import urllib.parse
import time
import hashlib
import re
import json

HOST = 'https://www.bilibili.com'
API_HOST = 'https://api.bilibili.com'

COMMON_PARAMS = {}

COMMON_HEADERS = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://www.bilibili.com/",
    "origin": "https://www.bilibili.com",
    "sec-ch-ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    # "sec-fetch-dest": "document",
    # "sec-fetch-mode": "navigate",
    # "sec-fetch-site": "same-origin",
    # "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

def common_request(host: str, uri: str, params: dict, headers: dict, doc: bool = False, need_sign: bool = False) -> tuple[dict, bool]:
    """
    请求 bilibili
    :param uri: 请求路径
    :param params: 请求参数
    :param headers: 请求头
    :param doc: 是否返回html
    :return: 返回数据和是否成功
    """
    url = f'{host}{uri}'
    cookie = headers.get('cookie', '')
    if cookie == '':
        cookie = headers.get('Cookie', '')
    params.update(COMMON_PARAMS)
    headers.update(COMMON_HEADERS)
    if COMMON_HEADERS.get('cookie', '') != '':
        headers['cookie'] = cookie + ";" + COMMON_HEADERS['cookie']
    else:
        headers['cookie'] = cookie

    if need_sign:
        params = sign(params)
    if doc:
        headers['accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"

    logger.info(
        f'url: {url}, request {url}, params={params}, headers={headers}')
    response = requests.get(url, params=params, headers=headers)
    # 设置服务器cookie
    set_cookies = "; ".join(f"{k}={v}" for k, v in response.cookies.get_dict().items())
    COMMON_HEADERS["cookie"] = set_cookies
    logger.info(
        f'url: {url}, params: {params}, response, code: {response.status_code}, body: {response.text}')

    if response.status_code != 200 or response.text == '':
        logger.error(
            f'url: {url}, params: {params}, request error, code: {response.status_code}, body: {response.text}')
        return {}, False
    
    if doc:
        return response.text, response.text != ''
    
    if response.json().get('code', 0) != 0:
        logger.error(
            f'url: {url}, params: {params}, request error, code: {response.status_code}, body: {response.text}')
        return response.json(), False

    return response.json(), True

def detail_request(id: str,  headers: dict) -> tuple[dict, bool]:
    """
    请求视频详情
    :param headers: 请求头
    :return: 返回数据和是否成功
    """
    document, succ = common_request(HOST, f'/video/{id}/', {}, headers, True)
    if not succ:
        return {}, succ
    try:
        # 下载信息
        soup = BeautifulSoup(document, 'html.parser')
        pattern = re.compile('window\\.__playinfo__.*')
        target = soup.head.find('script', text = pattern).text.replace('window.__playinfo__=', '')
        download_data = json.loads(target).get("data", {})
        # 视频信息
        pattern = re.compile('window\\.__INITIAL_STATE__=')
        target = soup.head.find('script', text = pattern).text.replace('window.__INITIAL_STATE__=', '').split(';')[0]
        detail_data = json.loads(target).get('videoData', {})
    except Exception as e:
        logger.error(f'parse hrml error, id: {id}, headers: {headers} doc: {document}, err: {e}')
        return {}, False
    
    data = {}
    data.update(download_data)
    data.update(detail_data)
    return data, True

def getMixinKey(key: str) -> str:
    salt = ""
    salt_map = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52]
    for pos in salt_map:
        salt += key[pos]
    return salt[:32]

def get_img_url_sub_url() -> str:
    """
    获取图片加密盐值
    """
    image_url = 'https://i0.hdslb.com/bfs/wbi/7cd084941338484aae1ad9425b84077c.png'
    sub_url = 'https://i0.hdslb.com/bfs/wbi/4932caff0ff746eab6f01bf08b70ac45.png'

    image_key = '7cd084941338484aae1ad9425b84077c'
    sub_key = '4932caff0ff746eab6f01bf08b70ac45'

    if 'get_salt_counter' not in globals():
        global get_salt_counter
        get_salt_counter = 0

    get_salt_counter += 1

    if get_salt_counter % 100000 == 0:
        url = 'https://api.bilibili.com/x/web-interface/nav'
        response = requests.get(url)
        if response.status_code != 200 or response.text == '':
            logger.error(
                f'url: {url}, request error, code: {response.status_code}, body: {response.text}')
            return getMixinKey(image_key + sub_key)
        wbi_img = response.json().get('data', {}).get('wbi_img', {})
        image_url, sub_url = wbi_img.get('img_url', image_url), wbi_img.get('sub_url', sub_url)
        image_key, sub_key = image_url.split('/')[-1].split('.')[0], sub_url.split('/')[-1].split('.')[0]

    return getMixinKey(image_key + sub_key)

def sign(params: dict):
    timestamp = int(time.time())
    params.update({"wts": timestamp})
    params = dict(sorted(params.items()))
    params = { k: ''.join(filter(lambda ch: ch not in "!'()*", str(v))) for k, v in params.items() }
    query = urllib.parse.urlencode(params)
    salt = get_img_url_sub_url()
    wbi_sign = hashlib.md5((query + salt).encode()).hexdigest()  # 计算 w_rid
    params['w_rid'] = wbi_sign
    return params