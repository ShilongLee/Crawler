from flask import request
from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_search
import random

def search():
    """
    获取淘宝商品搜索
    """
    keyword = request.args.get('keyword', '')
    page = int(request.args.get('page', 1))
    pagesize = int(request.args.get('pagesize', 48))
    _accounts = accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        res, succ = request_search(keyword, account.get('cookie', ''), page, pagesize)
        if not succ:
            accounts.expire(account.get('id', ''))
        if res == {} or not succ:
            continue
        logger.info(f'search success, keyword: {keyword}, page: {page}, pagesize: {pagesize}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'search failed, keyword: {keyword}, page: {page}, pagesize: {pagesize}')
    return reply(ErrorCode.INTERNAL_ERROR, '内部错误请重试')
