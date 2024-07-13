from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_detail
import random

# route
async def detail(id: str):
    """
    获取视频信息
    """
    _accounts = await accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        account_id = account.get('id', '')
        res, succ = await request_detail(id, account.get('cookie', ''))
        if res == {} or not succ:
            logger.error(f'get video detail failed. account: {account_id}, id: {id}')
            continue
        logger.info(f'get video detail success, account: {account_id}, id: {id}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'get video detail failed. id: {id}')
    return reply(ErrorCode.NO_ACCOUNT, '请先添加账号')