from .common import COMMON_HEADERS, APPKEY, HOST, sign, get_token
from lib.logger import logger
from lib import requests
from urllib.parse import quote
import json
import time
import re
import asyncio

async def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 48) -> dict:
    """
    请求taobao获取搜索信息
    """
    results = []
    page_size = 48
    start_page = int( offset / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    total = 0
    
    tasks = [search(keyword, cookie, page) for page in range(start_page, end_page + 1)]
    task_results = await asyncio.gather(*tasks)
    for data in task_results:
        results.extend(data.get('itemsArray', []))
        total = data.get('mainInfo', {}).get('totalResults', 0)

    ret = {'total': total, 'results': results[(offset % page_size):(offset % page_size + limit)]}
    return ret

def pack_search_query(cookie, keyword, page):
    quote_keyword = quote(keyword, 'utf-8')
    str_data = f'{{"appId":"34385","params":"{{\\"device\\":\\"HMA-AL00\\",\\"isBeta\\":\\"false\\",\\"grayHair\\":\\"false\\",\\"from\\":\\"nt_history\\",\\"brand\\":\\"HUAWEI\\",\\"info\\":\\"wifi\\",\\"index\\":\\"4\\",\\"rainbow\\":\\"\\",\\"schemaType\\":\\"auction\\",\\"elderHome\\":\\"false\\",\\"isEnterSrpSearch\\":\\"true\\",\\"newSearch\\":\\"false\\",\\"network\\":\\"wifi\\",\\"subtype\\":\\"\\",\\"hasPreposeFilter\\":\\"false\\",\\"prepositionVersion\\":\\"v2\\",\\"client_os\\":\\"Android\\",\\"gpsEnabled\\":\\"false\\",\\"searchDoorFrom\\":\\"srp\\",\\"debug_rerankNewOpenCard\\":\\"false\\",\\"homePageVersion\\":\\"v7\\",\\"searchElderHomeOpen\\":\\"false\\",\\"search_action\\":\\"initiative\\",\\"sugg\\":\\"_4_1\\",\\"sversion\\":\\"13.6\\",\\"style\\":\\"list\\",\\"ttid\\":\\"600000@taobao_pc_10.7.0\\",\\"needTabs\\":\\"true\\",\\"areaCode\\":\\"CN\\",\\"vm\\":\\"nw\\",\\"countryNum\\":\\"156\\",\\"m\\":\\"pc\\",\\"page\\":{page},\\"n\\":48,\\"q\\":\\"{quote_keyword}\\",\\"tab\\":\\"all\\",\\"pageSize\\":48,\\"sourceS\\":\\"0\\",\\"sort\\":\\"_coefp\\",\\"bcoffset\\":\\"\\",\\"ntoffset\\":\\"\\",\\"filterTag\\":\\"\\",\\"service\\":\\"\\",\\"prop\\":\\"\\",\\"loc\\":\\"\\",\\"start_price\\":null,\\"end_price\\":null,\\"startPrice\\":null,\\"endPrice\\":null,\\"itemIds\\":null,\\"p4pIds\\":null,\\"categoryp\\":\\"\\"}}"}}'
    quote_data = quote(str_data, 'utf-8')
    timestamp = str(time.time()).replace('.', '')[0:13]
    token = get_token(cookie)
    sgn = sign(token, timestamp, APPKEY, str_data)
    search_query = f'?jsv=2.7.2&appKey={APPKEY}&t={timestamp}&sign={sgn}&api=mtop.relationrecommend.wirelessrecommend.recommend&v=2.0&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data={quote_data}'
    logger.info(f'keyword: {keyword}, page: {page}, search_query: {search_query}')
    return search_query

async def search(keyword: str, cookie: str, page: int) -> dict:
    headers = {'cookie': cookie}
    headers.update(COMMON_HEADERS)
    query = pack_search_query(cookie, keyword, page)
    url = f'{HOST}/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/{query}'
    try:
        logger.info(f'request url: {url}')
        resp = await requests.get(url, headers=headers)
        logger.info(f'response url: {url}, body: {resp.text}')
        res_str = re.sub(r'^\s*mtopjsonp2\(|\)$', '', resp.text)
        res = json.loads(res_str)
        return res.get('data', {})
    except Exception as e:
        logger.error(f"failed to request {url}, error: {e}")
        return {}