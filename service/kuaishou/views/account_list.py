from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
def account_list():
    '''
    获取快手账号
    '''
    return reply(ErrorCode.OK, "OK", accounts.load())