from utils.error_code import ErrorCode
from utils.reply import reply
from lib.logger import logger
from ..logic import request_detail

# route
async def detail(id: str):
    """
    获取微博信息
    """
    # 微博可以游客访问，无cookie
    res, succ = await request_detail(id)
    if not succ:
        logger.error(f'get weibo detail failed, id: {id}, res: {res}')
        return reply(ErrorCode.INTERNAL_ERROR, '内部错误请重试')
    return reply(ErrorCode.OK, '成功', res)