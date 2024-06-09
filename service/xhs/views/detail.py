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
    获取笔记信息
    """
    id = request.args.get('id', '')

    _accounts = accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        res, succ = request_detail(id, account.get('cookie', ''))
        if not succ:
            accounts.expire(account.get('id', ''))
        if res == {} or not succ:
            continue
        logger.info(f'get note detail success, id: {id}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'get note detail failed, don\'t have enough effective account. id: {id}')
    return reply(ErrorCode.INTERNAL_ERROR, '内部错误请重试')