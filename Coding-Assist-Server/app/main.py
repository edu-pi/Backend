from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.config.settings import Settings
from app.web import exception_handlers
from app.route.advice.router import router as advice_router
from app.route.execute.router import router as execute_router
from app.web.logger import log_request, log_response

SWAGGER_HEADERS = {
    "title": "Coding Assist api",
    "version": "1.0.0",
}

app = FastAPI(
    swagger_ui_parameters={
        "deepLinking": True,
        "displayRequestDuration": True,
        "operationsSorter": "method",
        "filter": True,
        "tagsSorter": "alpha",
        "syntaxHighlight.theme": "tomorrow-night",
    },
    **SWAGGER_HEADERS
)

# 미들웨어 등록
app.middleware("http")(log_request)
if Settings.ENVIRONMENT == "dev":
    app.middleware("http")(log_response)

# 라우터 등록
app.include_router(advice_router,  prefix="/edupi-assist")
app.include_router(execute_router,  prefix="/edupi-assist")

# 핸들러 등록
exception_handlers.setup_exception_handlers(app)


@app.get("/edupi-assist/health-check", response_class=JSONResponse)
def root():
    return JSONResponse(
        status_code=200,
        content="ok")
