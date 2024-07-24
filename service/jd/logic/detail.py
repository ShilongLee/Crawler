import execjs
import json
from .common import HOST, COMMON_HEADERS
from lib import requests
from lib.logger import logger
from bs4 import BeautifulSoup

async def request_detail(id: str, cookie: str) -> dict:
    """
    请求jd获取商品详情
    """
    url = f'{HOST}/{id}.html'
    headers = {'Cookie': cookie, **COMMON_HEADERS}
    resp = await requests.get(url, headers=headers)
    logger.info(f"request detail url: {url}, headers: {headers}")
    if resp.status_code != 200 or resp.text == '':
        logger.error(f'request detail failed, url: {url}, code: {resp.status_code}, body: {resp.text}')
        return {}
    logger.info(f'request detail succ url: {url}, headers: {headers}, resp: {resp.text}')
    soup = BeautifulSoup(resp.text, 'html.parser')
    script_code = soup.head.find_all('script', charset='gbk')[0].text
    script_code += 'function jsonfy(){return JSON.stringify(pageConfig, null, 2);}'
    scrpit = execjs.compile(script_code)
    html_data = deal_detail_link(json.loads(scrpit.call('jsonfy')))
    return html_data

def deal_detail_link(html_data: dict) -> dict:
    """
    处理商品详情数据
    """
    product = html_data['product']
    product['href'] = 'https:' + product['href']
    product['src'] = 'https://img13.360buyimg.com/n1/' + product['src']
    for index, image in enumerate(product['imageList']):
        product['imageList'][index] = 'https://img13.360buyimg.com/n1/' + image
    product['colorApiDomain'] = 'https:' + product['colorApiDomain']
    product['easyBuyUrl'] = 'https:' + product['easyBuyUrl']
    product['desc'] = 'https:' + product['desc']
    product['foot'] = 'https:' + product['foot']
    product['askDoctorUrl'] = 'https:' + product['askDoctorUrl']
    return html_data