from flask import request
from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_user
import random

# route
def user():
    """
    获取用户信息
    """
    id = request.args.get('id', '')
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 20))

    _accounts = accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        res, succ = request_user(id, account.get('cookie', ''), offset, limit)
        if not succ:
            accounts.expire(account.get('id', ''))
        if res == {} or not succ:
            continue
        logger.info(f'get user detail success, id: {id}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'get user detail failed, don\'t have enough effective account. id: {id}')
    return reply(ErrorCode.INTERNAL_ERROR, '内部错误请重试')