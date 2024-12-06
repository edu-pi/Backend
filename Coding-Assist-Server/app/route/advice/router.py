from fastapi import APIRouter
from starlette.responses import JSONResponse

from app.route.advice.models.assist_request import AssistRequest
from app.web.models.success_reponse import SuccessResponse
from app.route.advice.service import ai_service

router = APIRouter()


@router.post("/v1/advice/correction")
async def correct(assist_request: AssistRequest):
    correct_response = await ai_service.correct(line=assist_request.line, code=assist_request.source_code)

    success_response = SuccessResponse(
        detail="success correct",
        result=correct_response.dict()
    )

    return JSONResponse(
        status_code=200,
        content=success_response.to_dict()
    )


@router.post("/v1/advice/hint")
async def hint(assist_request: AssistRequest):
    hint_response = await ai_service.hint(line=assist_request.line, code=assist_request.source_code)

    success_response = SuccessResponse(
        detail="success hint",
        result=hint_response.dict()
    )

    return JSONResponse(
        status_code=200,
        content=success_response.to_dict()
    )