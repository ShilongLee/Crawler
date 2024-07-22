import time
import hashlib
from urllib.parse import quote
from lib.logger import logger

HOST = 'https://h5api.m.taobao.com'

COMMON_HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Referer': 'https://s.taobao.com/search',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'script',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
}

APPKEY = '12574478'

def sign(token, tme, appKey, data):
    st = token+"&"+tme+"&"+appKey+"&"+data
    m = hashlib.md5(st.encode(encoding='utf-8')).hexdigest()
    return(m)

def get_token(cookie):
    get_cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
    _m_h5_tk = get_cookies['_m_h5_tk']
    token = _m_h5_tk.split('_')[0]
    return token
