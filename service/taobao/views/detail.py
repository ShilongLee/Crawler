from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_detail
import random

# route
async def detail(id: str):
    """
    获取商品详情
    """
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res = await request_detail(id, account.get('cookie', ''))
        if res == {}:
            logger.error(f'get item detail failed, account: {account_id}, id: {id}, res: {res}')
            continue
        logger.info(f'get item detail success, account: {account_id}, id: {id}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'get item detail failed. id: {id}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')