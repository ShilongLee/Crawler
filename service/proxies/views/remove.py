from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import proxies
from pydantic import BaseModel
from lib.logger import logger
from typing import List

class Param(BaseModel):
    ids: List[int]

async def remove(param: Param):
    '''
    移除代理地址
    '''
    failed_list = []
    for id in param.ids:
        result = await proxies.remove(id)
        if(not result):
            failed_list.append(id)
            logger.error(f"remove proxy failed, id: {id}")
    data = None
    if(len(failed_list) > 0):
        data = {"failed": failed_list}
    return reply(data = data)