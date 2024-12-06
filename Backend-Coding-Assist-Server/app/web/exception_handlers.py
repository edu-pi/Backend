from venv import logger

from openai import OpenAIError
from starlette import status
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.route.execute.exception.code_execute_error import CodeExecuteError
from app.route.execute.exception.code_syntax_error import CodeSyntaxError
from app.route.execute.exception.code_visualize_error import CodeVisualizeError
from app.web.exception.base_exception import BaseCustomException
from app.web.exception.enum.error_enum import ErrorEnum
from app.web.exception.invalid_exception import InvalidException
from app.route.advice.exception.openai_exception import OpenaiException
from app.web.exception.task_fail_exception import TaskFailException
from app.web.models.error_response import ErrorResponse


def setup_exception_handlers(app: FastAPI):
    @app.exception_handler(InvalidException)
    async def invalid_exception_handler(request: Request, exc: InvalidException):
        logger.info(f"[{exc.error_enum}] : code:{exc.error_enum.code}, detail:{exc.error_enum.detail}, {exc.args}")

        response = ErrorResponse(
            code=exc.error_enum.code,
            detail=exc.error_enum.detail,
            result=exc.result
        )
        return JSONResponse(
            status_code=exc.status,
            content=response.to_dict()
        )

    @app.exception_handler(OpenaiException)
    async def openai_exception_handler(request: Request, exc: OpenaiException):
        logger.error(f"[openai_exception] : code:{exc.error_enum.code}, detail:{exc.error_enum.detail}, {exc.args}")

        response = ErrorResponse(
            code=ErrorEnum.OPENAI_SERVER_ERROR.code,
            detail=exc.error_enum.detail,
            result=exc.result
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.to_dict()
        )

    @app.exception_handler(TaskFailException)
    async def task_fail_exception_handler(request: Request, exc: TaskFailException):
        logger.error(f"[Task fail Exception] : code:{exc.error_enum.code}, detail:{exc.error_enum.detail}, {exc.args}")

        response = ErrorResponse(
            code=ErrorEnum.UNKNOWN_ERROR.code,
            detail=ErrorEnum.UNKNOWN_ERROR.detail,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.to_dict()
        )

    @app.exception_handler(CodeExecuteError)
    @app.exception_handler(CodeSyntaxError)
    @app.exception_handler(CodeVisualizeError)
    async def code_error_exception_handler(request: Request,
                                           exc: CodeExecuteError | CodeSyntaxError | CodeVisualizeError):
        logger.info(f"[{exc.error_enum}] : code:{exc.error_enum.code}, detail:{exc.error_enum.detail}, {exc.args}")

        response = ErrorResponse(code=exc.error_enum.code, detail=exc.error_enum.detail, result=exc.result)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=response.to_dict())

    @app.exception_handler(Exception)
    async def exception_handler(request: Request, exc: Exception):
        logger.error(f"[Unknown Exception] : {exc.args}")
        response = ErrorResponse(
            code=ErrorEnum.UNKNOWN_ERROR.code,
            detail=ErrorEnum.UNKNOWN_ERROR.detail,
            result={}
        )

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=response.to_dict()
        )
