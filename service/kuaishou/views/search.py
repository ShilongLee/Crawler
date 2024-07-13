from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_search
import random

async def search(keyword: str, offset: int = 0, limit: int = 20):
    """
    获取视频搜索
    """
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res, succ = await request_search(keyword, account.get('cookie', ''), offset, limit)
        if res == {} or not succ:
            logger.error(f'search failed, account: {account_id}, keyword: {keyword}, offset: {offset}, limit: {limit}, res: {res}')
            continue
        logger.info(f'search success, account: {account_id}, keyword: {keyword}, offset: {offset}, limit: {limit}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'search failed, keyword: {keyword}, offset: {offset}, limit: {limit}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')