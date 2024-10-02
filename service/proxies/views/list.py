from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import proxies
async def list():
    '''
    返回代理地址
    '''
    return reply(ErrorCode.OK, "OK", await proxies.load())