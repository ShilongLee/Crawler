from .common import SEARCH_URL, COMMON_HEADERS
import requests
import json
import re
from lib.logger import logger
from urllib.parse import quote
from bs4 import BeautifulSoup

def request_search(keyword: str, cookie: str, page: int = 1) -> tuple[dict, bool]:
    """
    请求jd获取搜索信息
    """
    ret = []
    page = page * 2 - 1
    keyword = quote(keyword)
    query = f'?keyword={keyword}&page={page}'
    url = f'{SEARCH_URL}{query}'
    headers = {'cookie': cookie}
    headers.update(COMMON_HEADERS)
    try:
        logger.info(f'url: {url}')
        with requests.get(url, headers=headers) as res:
            html = res.text
            ret = parse_search_html(html)
            ret_count = len(ret)
            logger.info(f'ret_count: {ret_count}')
    except Exception as e:
        print(e)
        return {}, False

    return ret, True

findImgSrc = re.compile(r'<img.*data-lazy-img="(.*?)"', re.S)
findPrice = re.compile(r'<i>(.*?)</i>', re.S)
findInfo = re.compile(r'<div class="p-name p-name-type-2">(.*?)<em>(.*?)</em>', re.S)
findTag = re.compile(r'<span(.*?)>(.*?)</span>', re.S)
findStore = re.compile(r'<span class="J_im_icon"><a.*?>(.*?)</a>', re.S)
findSupply = re.compile(r'<i class="goods-icons J-picon-tips J-picon-fix" data-idx="1" data-tips="京东自营，品质保障">(.*?)</i>', re.S)
def parse_search_html(html):
    soup = BeautifulSoup(html, "html.parser")
    datalist = []
    for item in soup.find_all("li", class_="gl-item"):
        data = {}
        item = str(item)
        imgSrc = re.findall(findImgSrc, item)[0]
        imgSrc = imgSrc[2:]  # 去掉前面多余的/
        price = re.findall(findPrice, item)[0]
        data["imgSrc"] = imgSrc
        data["price"] = price
        info = re.findall(findInfo, item)[0]
        tmpTag = info[1]
        tag = re.findall(findTag, tmpTag)
        if len(tag) != 0:
            data["tag"] = tag[0][1]
            tmpTag = re.sub(tag[0][1], '', tmpTag)
        else:
            data["tag"] = ' '

        tmpTag = re.sub('<(.*?)>', '', tmpTag)  # 去掉多余符号
        tmpTag = re.sub('\n', '', tmpTag)
        tmpTag = re.sub('\t', '', tmpTag)
        data["title"] = tmpTag

        # ratNum = re.findall(findRatNum,item)
        store = re.findall(findStore, item)[0]
        data["store"] = store

        supply = re.findall(findSupply, item)
        if len(supply) != 0:
            data["supply"] = supply[0]
        else:
            data["supply"] = "第三方"
        datalist.append(data)
    return datalist

