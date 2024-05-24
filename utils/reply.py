from .error_code import ErrorCode
from flask import jsonify
def reply(code: ErrorCode = ErrorCode.OK, msg: str = "OK", data: dict = None):
    return jsonify({
        "code": code.value,
        "msg": msg,
        "data": data
    })