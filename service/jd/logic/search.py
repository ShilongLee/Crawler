import re
from .common import SEARCH_URL, COMMON_HEADERS
from lib import requests
from lib.logger import logger
from urllib.parse import quote
from bs4 import BeautifulSoup
from asyncio import gather

async def request_search(keyword: str, cookie: str, offset: int = 0, limit: int = 30) -> dict:
    """
    请求jd获取搜索信息
    """
    results = []
    page_size = 30
    start_page = int( offset / page_size ) + 1
    end_page = int((offset + limit - 1) / page_size) + 1
    keyword = quote(keyword)
    total = 0
    tasks = []
    for page_it in range(start_page, end_page + 1):
        page = page_it * 2 - 1
        tasks.append(search(keyword, page, cookie))
    task_results = await gather(*tasks)
    for data, _total in task_results:
        if _total != 0:
            total = _total
        results.extend(data)
    ret = {"results": results[(offset % page_size):(offset % page_size + limit)], "total": total}
    return ret

async def search(keyword: str, page: int, cookie: str) -> tuple[list, int]:
    query = f'?keyword={keyword}&page={page}'
    url = f'{SEARCH_URL}{query}'
    headers = {'cookie': cookie}
    headers.update(COMMON_HEADERS)
    try:
        logger.info(f'request url: {url}')
        resp = await requests.get(url, headers=headers)
        logger.info(f'response url: {url}, body: {resp.text}')
        ret, total = parse_search_html(resp.text)
        return ret, total
    except Exception as e:
        logger.error(f"failed to request {url}, error: {e}")
        return [], 0

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

