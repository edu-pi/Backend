from enum import Enum


class ErrorEnum(Enum):

    # 400
    TASK_FAIL = "CA-400001", "There is a problem with the service login"
    CODE_SYNTAX_ERROR = "CA-400002", "The code is incorrect syntax"
    CODE_CORRECT_FAIL = "CA-400003", "code correct fail"
    CODE_EXEC_ERROR = "CA-400004", "The format is not supported for security reasons"
    CODE_EXEC_SECURITY_ERROR = "CA-400004", "The format is not supported for security reasons"
    INPUT_SIZE_MATCHING_ERROR = "CA-400005", "The number of user inputs does not match."
    NOT_SUPPORTED_VISUALIZE = "CA-400006", "It contains syntax that we can't visualize yet."
    CODE_EXEC_TIMEOUT = "CA-400007", "The code execution is too long."
    CODE_VIZ_TIMEOUT = "CA-400007", "The code visualization is too long."

    UNKNOWN_ERROR = "CA-400999", "The unexpected error"     # Exception으로 잡힐 때 해당 코드 사용


    #500
    CODE_EXEC_SERVER_ERROR = "CA-503001", "There is a problem with the execute service login"
    OPENAI_SERVER_ERROR = "CA-504001", "Open AI internal server error"
    OPENAI_MAX_TOKEN_LIMIT = "CA-504002", "Open AI max token limit"


    def __init__(self, code, detail):
        self.code = code
        self.detail = detail

    def to_dict(self):
        return {
            "code": self.code,
            "detail": self.detail,
        }
