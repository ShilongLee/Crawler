from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
async def account_list():
    '''
    获取微博账号
    '''
    return reply(ErrorCode.OK, "OK", await accounts.load())