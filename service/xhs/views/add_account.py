from flask import request
from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger

def add_account():
    '''
    添加小红书账号
    '''
    id = request.json.get('id', '')
    cookie = request.json.get('cookie', '')
    if id == '' or cookie == '':
        logger.error(f'id or cookie is empty, id: {id}, cookie: {cookie}')
        return reply(ErrorCode.PARAMETER_ERROR, "id and cookie is required")
    
    accounts.save(id, cookie, 0)
    logger.info(f'xhs add account, id: {id}, cookie: {cookie}')
    return reply()