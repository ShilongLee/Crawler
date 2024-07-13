from lib.logger import logger
from bs4 import BeautifulSoup
from lib import requests
import urllib.parse
import time
import hashlib
import re
import json
import random

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


async def common_request(host: str, uri: str, params: dict, headers: dict, doc: bool = False, need_sign: bool = False) -> tuple[dict, bool]:
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
        params = await sign(params)
    if doc:
        headers['accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"

    logger.info(
        f'url: {url}, request {url}, params={params}, headers={headers}')
    response = await requests.get(url, params=params, headers=headers)
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


def extract_outermost_json(text):
    # 尝试从字符串的不同长度解析JSON，直到成功
    for i in range(len(text), 0, -1):
        try:
            # 尝试解析前i个字符
            json_obj = json.loads(text[:i])
            return json_obj
        except json.JSONDecodeError:
            # 如果解析失败，继续尝试下一个长度
            continue
    raise ValueError("No valid JSON found")


async def detail_request(id: str,  headers: dict) -> tuple[dict, bool]:
    """
    请求视频详情
    :param headers: 请求头
    :return: 返回数据和是否成功
    """
    document, succ = await common_request(HOST, f'/video/{id}/', {}, headers, True)
    if not succ:
        return {}, succ
    try:
        # 下载信息
        soup = BeautifulSoup(document, 'html.parser')
        pattern = re.compile('window\\.__playinfo__.*')
        target = soup.head.find('script', text=pattern).text.replace(
            'window.__playinfo__=', '')
        download_data = json.loads(target).get("data", {})
        # 视频信息
        pattern = re.compile('window\\.__INITIAL_STATE__=')
        target = extract_outermost_json(soup.head.find(
            'script', text=pattern).text.replace('window.__INITIAL_STATE__=', ''))
        detail_data = target.get('videoData', {})
    except Exception as e:
        logger.error(f'parse hrml error, id: {id}, headers: {headers} doc: {document}, err: {e}')
        return {}, False

    data = {}
    data.update(download_data)
    data.update(detail_data)
    return data, True


def getMixinKey(key: str) -> str:
    salt = ""
    salt_map = [46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49, 33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41,
                13, 37, 48, 7, 16, 24, 55, 40, 61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11, 36, 20, 34, 44, 52]
    for pos in salt_map:
        salt += key[pos]
    return salt[:32]


async def get_img_url_sub_url() -> str:
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
        response = await requests.get(url)
        if response.status_code != 200 or response.text == '':
            logger.error(
                f'url: {url}, request error, code: {response.status_code}, body: {response.text}')
            return getMixinKey(image_key + sub_key)
        wbi_img = response.json().get('data', {}).get('wbi_img', {})
        image_url, sub_url = wbi_img.get(
            'img_url', image_url), wbi_img.get('sub_url', sub_url)
        image_key, sub_key = image_url.split(
            '/')[-1].split('.')[0], sub_url.split('/')[-1].split('.')[0]

    return getMixinKey(image_key + sub_key)


async def sign(params: dict):
    timestamp = int(time.time())
    params.update({"wts": timestamp})
    params = dict(sorted(params.items()))
    params = {k: ''.join(filter(lambda ch: ch not in "!'()*", str(v)))
              for k, v in params.items()}
    query = urllib.parse.urlencode(params)
    salt = await get_img_url_sub_url()
    wbi_sign = hashlib.md5((query + salt).encode()).hexdigest()  # 计算 w_rid
    params['w_rid'] = wbi_sign
    return params


def random_cacl_1(a, b) -> list:
    random_search_seed = random.randint(0, 114)
    return [2 * a + 2 * b + 3 * random_search_seed, 4 * a - b + random_search_seed, random_search_seed]


def random_cacl_2(a, b) -> list:
    random_search_seed = random.randint(0, 514)
    return [3 * a + 2 * b + random_search_seed, 4 * a - 4 * b + 2 * random_search_seed, random_search_seed]


def gen_location() -> list:
    timestamp = random.randint(5000, 6000)
    pre_x, pre_y = 0, 0
    st_x, st_y = random.randint(500, 600), random.randint(200, 400)
    ed_x, ed_y = 641, 773
    location_list = []
    for _ in range(0, 8):
        location_list.append({
            'type': 'mousemove',
            'preX': pre_x,
            'preY': pre_y,
            'x': st_x,
            'y': st_y,
            'time': timestamp
        })
        pre_x = st_x
        pre_y = st_y
        st_x += random.randint(0, 50)
        st_y += random.randint(0, 50)
        timestamp += random.randint(100, 1000)

    location_list[-1]['x'], location_list[-1]['y'] = ed_x, ed_y
    ret = []
    for index, location in enumerate(location_list):
        ret.append(sign_localtion(
            location['x'], location['y'], location['time'], location['type'], index))
    return ret


def sign_localtion(x, y, timestamp, _, index):
    index = index * random.randint(0, 114)
    if x == 0 and y == 0:
        return {"x": 6 * index, "y": -index, "z": index, "timestamp": timestamp, "k": random.randint(0, 67)+60, "type": 0}
    return {"x": 3 * x + 2 * y + index, "y": 4 * x - 5 * y + index, "z": index, "timestamp": timestamp, "k": random.randint(0, 67)+60, "type": 0}


def get_dm_img(need_ds: bool = True) -> dict:
    dm_img_list = gen_location()
    dm_img_str = 'V2ViR0wgMS4wIChPcGVuR0wgRVMgMi4wIENocm9taXVtKQ'
    dm_cover_img_str = 'QU5HTEUgKEFwcGxlLCBBTkdMRSBNZXRhbCBSZW5kZXJlcjogQXBwbGUgTTEgUHJvLCBVbnNwZWNpZmllZCBWZXJzaW9uKUdvb2dsZSBJbmMuIChBcHBsZS'
    width = 1512
    height = 824
    search_top = 274
    search_left = 541
    search_width = 134
    search_height = 30
    video_top = 348
    video_left = 135
    video_width = 880
    video_height = 320
    random_search_p = random_cacl_1(search_top, search_left)
    random_search_s = random_cacl_2(search_width, search_height)
    random_video_p = random_cacl_1(video_top, video_left)
    random_video_s = random_cacl_2(video_width, video_height)
    dm_img_inter = {"ds": [
        {
            "t": 2,
            "c": "Y2xlYXJmaXggZy1zZWFyY2ggc2VhcmNoLWNvbnRhaW5lcg",
            "p": [random_video_p[0], random_video_p[2], random_video_p[1]],
            "s": [random_video_s[2], random_video_s[0], random_video_s[1]]
        },
        {
            "t": 2,
            "c": "c2VjdGlvbiB2aWRlbyBsb2FkaW5nIGZ1bGwtcm93cw",
            "p": [random_search_p[0], random_search_p[2], random_search_p[1]],
            "s": [random_search_s[2], random_search_s[0], random_search_s[1]]
        }
    ],
        "wh": random_cacl_1(width, height),
        "of": random_cacl_2(0, 0)
    }
    if not need_ds:
        dm_img_inter["ds"] = []
    return {"dm_img_list": json.dumps(dm_img_list).replace(' ', ''), "dm_img_str": dm_img_str, "dm_cover_img_str": dm_cover_img_str, "dm_img_inter": json.dumps(dm_img_inter).replace(' ', '')}