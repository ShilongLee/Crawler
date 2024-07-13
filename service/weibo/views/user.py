from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_user
import random

# route
async def user(id: str, offset: int = 0, limit: int = 5):
    """
    获取用户信息
    """
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res = await request_user(id, account.get('cookie', ''), offset, limit)
        logger.info(f'get user detail success, account: {account_id}, id: {id}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'get user detail failed. id: {id}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')