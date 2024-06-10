from .common import SEARCH_URL, COMMON_HEADERS
import requests
import json
import re
from lib.logger import logger
from urllib.parse import quote
from bs4 import BeautifulSoup

def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 30) -> tuple[dict, bool]:
    """
    请求jd获取搜索信息
    """
    results = []
    page_size = 30
    start_page = int((offset - 1) / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    keyword = quote(keyword)
    headers = {'cookie': cookie}
    headers.update(COMMON_HEADERS)
    total = 0
    for page_it in range(start_page, end_page + 1):
        page = page_it * 2 - 1
        query = f'?keyword={keyword}&page={page}'
        url = f'{SEARCH_URL}{query}'
        try:
            logger.info(f'request url: {url}')
            with requests.get(url, headers=headers) as res:
                logger.info(f'response url: {url}, body: {res.text}')
                html = res.text
                ret, total = parse_search_html(html)
                results.extend(ret)
        except Exception as e:
            logger.error(f"failed to request {url}, error: {e}")
            return {}, False
    ret = {"results": results[(offset % page_size):(offset % page_size + limit)], "total": total}
    return ret, True
def parse_search_html(html) -> tuple[list, int]:
    soup = BeautifulSoup(html, "html.parser")
    datalist = []
    src = soup.head.find_all("script")[-1].text.replace("\n", '').replace("\t", '').replace('\\\'','\'')
    total = int(re.search(r"result_count:'(\d+)'", src).group(1))
    for item in soup.find_all("li", class_="gl-item"):
        imgSrc = "https:" + item.find("div", class_="p-img").find("img")['data-lazy-img']
        price = item.find("div", class_="p-price").find("i").text
        info = {"title": item.find("div", class_="p-name p-name-type-2").find("em").text.replace(r"\t", '').replace(r'\n', ''), "link": "https:"+ item.find("div", class_="p-name p-name-type-2").find("a")["href"]}
        tag_span = item.find("div", class_="p-name p-name-type-2").find("em").find("span")
        tag = '' if not tag_span else tag_span.text
        store = {"title": item.find("div", class_="p-shop").find("span").text, "link": "https:"+ item.find("div", class_="p-shop").find("span").find("a")["href"]}
        supply = []
        for child in item.find("div", class_="p-icons"):
            text = child.text.replace('\t', '').replace('\n','')
            if text == '':
                continue
            supply.append(text)
        data = {
            "imgSrc": imgSrc,
            "price": price,
            "info": info,
            "tag": tag,
            "store": store,
            "supply": supply,
        }
        datalist.append(data)
    return datalist, total

