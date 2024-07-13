from enum import Enum

class ErrorCode(Enum):
    OK = 0
    PARAMETER_ERROR = 1
    INTERNAL_ERROR = 2
    NO_ACCOUNT = 3