from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_comments
import random

async def comments(id: str, offset: int = 0, limit: int = 20):
    """
    获取微博评论
    """
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res, succ = await request_comments(id, account.get('cookie', ''), offset, limit)
        if not succ:
            await accounts.expire(account.get('id', ''))
        if res == {} or not succ:
            logger.error(f'get comments failed, account: {account_id}, id: {id}, offset: {offset}, limit: {limit}, res: {res}')
            continue
        logger.info(f'get comments success, account: {account_id}, id: {id}, offset: {offset}, limit: {limit}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'get comments failed. id: {id}, offset: {offset}, limit: {limit}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')