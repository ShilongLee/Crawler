from utils.reply import reply
from ..models import proxies
from pydantic import BaseModel
from lib.logger import logger
from typing import List

class Param(BaseModel):
    urls: List[str]

async def add(param: Param):
    '''
    增加代理地址，默认开启使用
    '''
    for url in param.urls:
        await proxies.save(url, 1)
        logger.info(f'add proxy, url: {url}')
    return reply()