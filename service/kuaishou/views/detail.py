from flask import request
from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_detail
import random

# route
def detail():
    """
    获取视频信息
    """
    id = request.args.get('id', '')

    _accounts = accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        res, expired = request_detail(id, account.get('cookie', ''))
        if expired:
            accounts.expire(account.get('id', ''))
        if res == {} or expired:
            continue
        logger.info(f'get video detail success, id: {id}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'get video detail failed, don\'t have enough effective account. id: {id}')
    return reply(ErrorCode.INTERNAL_ERROR, '内部错误请重试')