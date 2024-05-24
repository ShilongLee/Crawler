from enum import Enum
from lib.logger import logger
import requests

HOST = 'https://www.kuaishou.com'

COMMON_HEADERS = {
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "DNT": "1",
    "Origin": "https://www.kuaishou.com",
    "Pragma": "no-cache",
    "Referer": "https://www.kuaishou.com/new-reco",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "accept": "*/*",
    "content-type": "application/json",
    "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"'
}

GRAPHQL_DIR = 'service/kuaishou/logic/graphql/'


class GraphqlQuery(Enum):
    SEARCH = 'search'
    DETAIL = 'detail'
    COMMENTS = 'comments'

GRAPHQL_FILES = {
    GraphqlQuery.SEARCH: 'search_query.graphql',
    GraphqlQuery.DETAIL: 'video_detail.graphql',
    GraphqlQuery.COMMENTS: 'comment_list.graphql',
    }


graphql = {}
for type, file in GRAPHQL_FILES.items():
    with open(str(GRAPHQL_DIR + file), 'r') as f:
        graphql_queries = f.read()
        graphql[type] = graphql_queries

def load_graphql_queries(type: GraphqlQuery) -> str:
    return graphql.get(type)

def common_request(data: dict, headers: dict) -> tuple[dict, bool]:
    url = f'{HOST}/graphql'
    headers.update(COMMON_HEADERS)

    logger.info(
        f'url: {url}, request {url}, body={data}, headers={headers}')
    response = requests.post(url, json=data, headers=headers)
    logger.info(
        f'url: {url}, body: {data}, response, code: {response.status_code}, body: {response.text}')

    if response.status_code != 200 or response.text == '':
        logger.error(
            f'url: {url}, body: {data}, request error, code: {response.status_code}, body: {response.text}')
        return {}, False
    if response.json().get('status_code', 0) != 0:
        logger.error(
            f'url: {url}, body: {data}, request error, code: {response.status_code}, body: {response.text}')
        return response.json(), True

    return response.json(), False