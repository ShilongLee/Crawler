from flask import request
from utils.error_code import ErrorCode
from utils.reply import reply
from ..models import accounts
from lib.logger import logger
from ..logic import request_replys
import random

def replys():
    """
    获取笔记评论回复
    """
    id = request.args.get('id', '')
    comment_id = request.args.get('comment_id', '')
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))
    _accounts = accounts.load()
    random.shuffle(_accounts)
    for account in _accounts:
        if account.get('expired', 0) == 1:
            continue
        res, succ = request_replys(id, comment_id, account.get('cookie', ''), offset, limit)
        if not succ:
            accounts.expire(account.get('id', ''))
        if res == {} or not succ:
            continue
        logger.info(f'get reply success, id: {id}, comment_id: {comment_id}, offset: {offset}, limit: {limit}, res: {res}')
        return reply(ErrorCode.OK, '成功' , res)
    logger.warning(f'get reply failed, id: {id}, comment_id: {comment_id}, offset: {offset}, limit: {limit}')
    return reply(ErrorCode.INTERNAL_ERROR, '内部错误请重试')