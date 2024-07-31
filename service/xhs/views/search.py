from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_search
import random

async def search(keyword: str, sort: str = "general", offset: int = 0, limit: int = 20):
    """
    获取笔记搜索
    "sort": general：默认, popularity_descending：最热, time_descending：最新
    """
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res = await request_search(keyword, account.get('cookie', ''), sort, offset, limit)
        logger.info(f'search success, account: {account_id}, keyword: {keyword}, sort: {sort}, offset: {offset}, limit: {limit}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'search failed. keyword: {keyword}, sort: {sort}, offset: {offset}, limit: {limit}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')