from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from pydantic import BaseModel

class Param(BaseModel):
    id: str
    cookie: str

async def add_account(param: Param):
    '''
    添加快手账号
    '''
    if param.id == '' or param.cookie == '':
        logger.error(f'id or cookie is empty, id: {param.id}, cookie: {param.cookie}')
        return reply(ErrorCode.PARAMETER_ERROR, "id and cookie is required")
    
    await accounts.save(param.id, param.cookie, 0)
    logger.info(f'kuaishou add account, id: {param.id}, cookie: {param.cookie}')
    return reply()