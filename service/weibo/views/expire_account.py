from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from pydantic import BaseModel

class Param(BaseModel):
    id: str

async def expire_account(param: Param):
    '''
    设置微博账号过期
    '''
    await accounts.expire(param.id)
    return reply(ErrorCode.OK, "OK", None)