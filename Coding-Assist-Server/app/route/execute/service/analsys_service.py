
import requests
from app.config.settings import Settings
from app.route.execute.exception.code_visualize_error import CodeVisualizeError
from app.web.exception.enum.error_enum import ErrorEnum
from app.web.exception.task_fail_exception import TaskFailException


def analyze_code(source_code: str, user_input: str):
    visualise_url = "/".join([Settings.ENGINE_SERVER, "v1", "python"])
    try:
        response = requests.post(
            visualise_url,
            json={"source_code": source_code, "input": user_input}
        )
        response.raise_for_status()  # HTTPError 발생시 예외
        return response.json().get("result").get("code")

    except requests.exceptions.HTTPError as e:
        error_code = response.json().get("code")

        if error_code == 'CV-400001':
            raise CodeVisualizeError(ErrorEnum.NOT_SUPPORTED_VISUALIZE)
        elif error_code == 'CV-400002':
            raise CodeVisualizeError(ErrorEnum.CODE_VIZ_TIMEOUT)
        else:
            raise TaskFailException(ErrorEnum.TASK_FAIL)

