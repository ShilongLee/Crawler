import httpx
import json
import time
from data.driver import Proxies
            
proxyModel = Proxies("data/proxies/proxies.db")
proxies = []

class Response:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text

    def json(self):
        return json.loads(self.text)

def retry_request(func, max_retries=3):
    async def wrapper(*args, **kwargs):
        retries = 0
        while retries < max_retries:
            try:
                return await func(*args, **kwargs)
            except (httpx.ConnectError, httpx.ReadTimeout) as e:
                retries += 1
        raise Exception(f"Failed after {max_retries} retries")

    return wrapper

async def get_proxy():
    global proxies
    proxies = await proxyModel.load(enable = 1)
    if(len(proxies) == 0):
        return None
    proxy = proxies[int(int(time.time()) / 300) % len(proxies)]
    return proxy['url']

@retry_request
async def get(url, headers=None, params=None) -> Response:
    proxy = await get_proxy()
    async with httpx.AsyncClient(proxy=proxy) as client:
        response = await client.get(url, headers=headers, params=params)
        return Response(response.status_code, response.text)

@retry_request
async def post(url, headers=None, data=None, json=None) -> Response:
    proxy = await get_proxy()
    async with httpx.AsyncClient(proxy=proxy) as client:
        response = await client.post(url, headers=headers, json=json, data=data)
        return Response(response.status_code, response.text)
