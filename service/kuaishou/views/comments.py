from flask import request
from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_comments
import random

def comments():
    """
    获取视频评论
    """
    id = request.args.get('id', '')
    pcursor = request.args.get('pcursor', '')

    _accounts = accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        res, expired = request_comments(id, account.get('cookie', ''), pcursor)
        if expired:
            accounts.expire(account.get('id', ''))
        if res == {} or expired:
            continue
        logger.info(f'get comments success, id: {id}, pcursor: {pcursor}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'get comments failed, don\'t have enough effective account. id: {id}, pcursor: {pcursor}')
    return reply(ErrorCode.INTERNAL_ERROR, '内部错误请重试')