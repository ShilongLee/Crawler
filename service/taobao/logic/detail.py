from .common import COMMON_HEADERS, APPKEY, HOST, get_token, sign
from lib.logger import logger
from lib import requests
from urllib.parse import quote
import time

async def request_detail(id: str, cookie: str) -> dict:
    """
    请求taobao获取商品详情
    """
    str_data = f'{{"id":"{id}","detail_v":"3.3.2","exParams":"{{\\"id\\":\\"{id}\\",\\"item_type\\":\\"ad\\",\\"ali_refid\\":\\"a3_431358_1007:15572659:H:15572659_0_11770813889:c0a3730368049201836ac06218cb19dd\\",\\"ali_trackid\\":\\"296_c0a3730368049201836ac06218cb19dd\\",\\"spm\\":\\"a21bo.jianhua/a.201876.d5\\",\\"scm\\":\\"1007.40986.397407.0\\",\\"queryParams\\":\\"ali_refid=a3_431358_1007%3A15572659%3AH%3A15572659_0_11770813889%3Ac0a3730368049201836ac06218cb19dd&ali_trackid=296_c0a3730368049201836ac06218cb19dd&id={id}&item_type=ad&scm=1007.40986.397407.0&spm=a21bo.jianhua%2Fa.201876.d5\\",\\"domain\\":\\"https://item.taobao.com\\",\\"path_name\\":\\"/item.htm\\"}}"}}'
    quote_data = quote(str_data, 'utf-8')
    token = get_token(cookie)
    timestamp = str(time.time()).replace('.', '')[0:13]
    sgn = sign(token, timestamp, APPKEY, str_data)
    param = {
        'jsv': '2.6.1',
        'appKey': APPKEY,
        't': timestamp,
        'sign': sgn,
        'api': 'mtop.taobao.pcdetail.data.get',
        'v': '1.0',
        'isSec': '0',
        'ecode': '0',
        'timeout': '10000',
        'ttid': '2022@taobao_litepc_9.17.0',
        'AntiFlood': 'true',
        'AntiCreep': 'true',
        'dataType': 'json',
        'valueType': 'string',
        'preventFallback': 'true',
        'type': 'json',
        'data': quote_data
    }
    headers = {'cookie': cookie}
    headers.update(COMMON_HEADERS)
    url = f'{HOST}/h5/mtop.taobao.pcdetail.data.get/1.0/'
    logger.info(f'请求商品详情, url: {url}, params: {param}')
    resp = await requests.get(url, headers=headers, params=param)
    logger.info(f'请求商品详情, code: {resp.status_code}, body: {resp.json()}, url: {url}, params: {param}')
    if resp.status_code != 200:
        logger.error(f'请求商品详情失败, status_code: {resp.status_code}')
        return {}
    return resp.json().get('data')