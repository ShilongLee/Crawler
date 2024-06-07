import requests
import time
import hashlib
from urllib.parse import quote

SEARCH_API = 'mtop.relationrecommend.wirelessrecommend.recommend'
SEARCH_URL = f'https://h5api.m.taobao.com/h5/{SEARCH_API}/2.0/'
APPKEY = '12574478'
SEARCH_JSV = '2.7.2'
SEARCH_V = '2.0'

def pack_search_query(cookie, keyword, page, page_size):
    quote_keyword = quote(keyword, 'utf-8')
    str_data = f'{{"appId":"34385","params":"{{\\"device\\":\\"HMA-AL00\\",\\"isBeta\\":\\"false\\",\\"grayHair\\":\\"false\\",\\"from\\":\\"nt_history\\",\\"brand\\":\\"HUAWEI\\",\\"info\\":\\"wifi\\",\\"index\\":\\"4\\",\\"rainbow\\":\\"\\",\\"schemaType\\":\\"auction\\",\\"elderHome\\":\\"false\\",\\"isEnterSrpSearch\\":\\"true\\",\\"newSearch\\":\\"false\\",\\"network\\":\\"wifi\\",\\"subtype\\":\\"\\",\\"hasPreposeFilter\\":\\"false\\",\\"prepositionVersion\\":\\"v2\\",\\"client_os\\":\\"Android\\",\\"gpsEnabled\\":\\"false\\",\\"searchDoorFrom\\":\\"srp\\",\\"debug_rerankNewOpenCard\\":\\"false\\",\\"homePageVersion\\":\\"v7\\",\\"searchElderHomeOpen\\":\\"false\\",\\"search_action\\":\\"initiative\\",\\"sugg\\":\\"_4_1\\",\\"sversion\\":\\"13.6\\",\\"style\\":\\"list\\",\\"ttid\\":\\"600000@taobao_pc_10.7.0\\",\\"needTabs\\":\\"true\\",\\"areaCode\\":\\"CN\\",\\"vm\\":\\"nw\\",\\"countryNum\\":\\"156\\",\\"m\\":\\"pc\\",\\"page\\":{page},\\"n\\":{page_size},\\"q\\":\\"{quote_keyword}\\",\\"tab\\":\\"all\\",\\"pageSize\\":{page_size},\\"sourceS\\":\\"0\\",\\"sort\\":\\"_coefp\\",\\"bcoffset\\":\\"\\",\\"ntoffset\\":\\"\\",\\"filterTag\\":\\"\\",\\"service\\":\\"\\",\\"prop\\":\\"\\",\\"loc\\":\\"\\",\\"start_price\\":null,\\"end_price\\":null,\\"startPrice\\":null,\\"endPrice\\":null,\\"itemIds\\":null,\\"p4pIds\\":null,\\"categoryp\\":\\"\\"}}"}}'
    quote_data = quote(str_data, 'utf-8')
    timestamp = str(time.time()).replace('.', '')[0:13]
    token = get_token(cookie)
    sgn = sign(token, timestamp, APPKEY, str_data)
    search_query = f'?jsv={SEARCH_JSV}&appKey={APPKEY}&t={timestamp}&sign={sgn}&api={SEARCH_API}&v={SEARCH_V}&type=jsonp&dataType=jsonp&callback=mtopjsonp2&data={quote_data}'
    print(search_query)
    return search_query

def sign(token, tme, appKey, data):
    st = token+"&"+tme+"&"+appKey+"&"+data
    m = hashlib.md5(st.encode(encoding='utf-8')).hexdigest()
    return(m)

def convert_cookies_to_dict(cookies):
    cookies = dict([l.split("=", 1) for l in cookies.split("; ")])
    return cookies

def get_token(cookie):
    get_cookies = convert_cookies_to_dict(cookie)
    _m_h5_tk = get_cookies['_m_h5_tk']
    token = _m_h5_tk.split('_')[0]
    return token
