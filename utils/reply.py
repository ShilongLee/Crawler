from .error_code import ErrorCode

def reply(code: ErrorCode = ErrorCode.OK, msg: str = "OK", data: dict = None):
    return {
        "code": code.value,
        "msg": msg,
        "data": data
    }