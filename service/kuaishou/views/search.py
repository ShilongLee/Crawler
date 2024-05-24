from flask import request
from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_search
import random

def search():
    """
    获取视频搜索
    """
    keyword = request.args.get('keyword', '')
    pcursor = request.args.get('pcursor', '')

    _accounts = accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        res, expired = request_search(keyword, account.get('cookie', ''), pcursor)
        if expired:
            accounts.expire(account.get('id', ''))
        if res == {} or expired:
            continue
        logger.info(f'search success, keyword: {keyword}, pcursor: {pcursor}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'search failed, keyword: {keyword}, pcursor: {pcursor}')
    return reply(ErrorCode.INTERNAL_ERROR, '内部错误请重试')