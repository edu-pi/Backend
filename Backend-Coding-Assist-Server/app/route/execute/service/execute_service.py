import re
import subprocess

from app.route.execute.exception.code_execute_error import CodeExecuteError
from app.route.execute.exception.code_syntax_error import CodeSyntaxError
from app.web.exception.enum.error_enum import ErrorEnum
from app.web.exception.task_fail_exception import TaskFailException
from app.web.logger import logger

FORBIDDEN_IMPORTS = ["os", "sys", "subprocess", "shutil"]


def execute_code(source_code: str, user_input: str):
    if _contains_forbidden_imports(source_code):
        # 보안상 실행 안함
        raise CodeExecuteError(ErrorEnum.CODE_EXEC_SECURITY_ERROR)

    try:
        process = subprocess.run(
            args=["python3", "-c", source_code],
            input=user_input,
            capture_output=True,  # stdout, stderr 별도의 Pipe에서 처리
            timeout=1,  # limit child process execute time
            check=True,  # CalledProcessError exception if return_code is 0
            text=True
        )
        return process.stdout

    # 프로세스 실행 중 비정상 종료
    except subprocess.CalledProcessError as e:
        line_number = _get_error_line_number(e.stderr)
        if _is_input_missmatch(e.stderr):
            raise CodeExecuteError(ErrorEnum.INPUT_SIZE_MATCHING_ERROR)

        raise CodeSyntaxError(ErrorEnum.CODE_SYNTAX_ERROR, {"lineNumber": line_number, "errorMessage": e.stderr})

    except subprocess.TimeoutExpired as e:
        raise CodeExecuteError(ErrorEnum.CODE_EXEC_TIMEOUT)

    except Exception as e:
        logger.error("[Unexpected Exception] execute_code() {e.__class__.args}")
        raise TaskFailException(ErrorEnum.CODE_EXEC_SERVER_ERROR, e.args[0])


def _is_input_missmatch(error_msg):
    if "EOF when reading" in error_msg:
        return True
    return False

def _get_error_line_number(error_msg):
    matches = re.findall(r'line (\d+), in', error_msg)
    if matches:
        return matches[-1]

    matches = re.findall(r'line (\d+)', error_msg)
    return matches[-1] if matches else 1


def _contains_forbidden_imports(code: str) -> bool:
    # 금지된 모듈이 코드에 있는지 확인
    for module in FORBIDDEN_IMPORTS:
        if re.search(rf'\bimport\s+{module}\b', code):
            return True
    return False
