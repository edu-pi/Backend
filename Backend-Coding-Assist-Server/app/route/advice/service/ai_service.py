import aiofiles
from json import loads, JSONDecodeError
from os import path
from time import sleep
from openai import APITimeoutError, AsyncOpenAI

from app.config.settings import Settings
from app.route.advice.models.correct_response import CorrectResponse
from app.route.advice.models.hint_response import HintResponse
from app.web.exception.enum.error_enum import ErrorEnum
from app.route.advice.exception.openai_exception import OpenaiException
from app.web.exception.task_fail_exception import TaskFailException
from app.web.logger import logger


async def correct(line: int, code: str) -> CorrectResponse:
    template_path = path.join(path.dirname(__file__), 'prompts', 'correct_template.txt')
    template = await _load_template(template_path)

    print(line)
    prompt = template.format(line=line, code=code)
    response_data = await _call_openai_api(prompt)

    return await CorrectResponse.of(response_data, line)


async def hint(line: int, code: str) -> HintResponse:
    template_path = path.join(path.dirname(__file__), 'prompts', 'hint_template.txt')
    template = await _load_template(template_path)

    prompt = template.format(line=line, code=code)
    response_data = await _call_openai_api(prompt)

    return await HintResponse.of(response_data)


async def _load_template(file_path) -> str:
    async with aiofiles.open(file_path, 'r') as file:
        return await file.read()


async def _call_openai_api(prompt: str,  max_retries: int = 2, delay: int = 2) -> dict:
    retries = 0
    client = AsyncOpenAI(api_key=Settings.OPEN_API_KEY, timeout=3, max_retries=max_retries)

    while retries < max_retries:
        try:
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                ],
                max_tokens=2000,
                n=1,  # 한 질문에 응답의 개수
                stop=None,  # 모델 중단 기준 문자열
                temperature=0.4,  # 같은 질문에 일관성 정도 (0~1 : 높을수록 창의적인 답변)
                response_format={"type": "json_object"}
            )
            return loads(response.choices[0].message.content)

        except JSONDecodeError as e:
            logger.error(f"OpenAI: {e}. Request failed due to exceeding max token limit")
            raise OpenaiException(ErrorEnum.OPENAI_MAX_TOKEN_LIMIT, e)

        except APITimeoutError as e:
            retries += 1
            if retries < max_retries:
                logger.error(f"OpenAI: {e}. Request failed due to Server error. retry after {delay}s ({retries}/{max_retries})")
                sleep(delay)
            else:
                raise OpenaiException(ErrorEnum.OPENAI_SERVER_ERROR)

        except Exception as e:
            raise TaskFailException(ErrorEnum.OPENAI_SERVER_ERROR)


