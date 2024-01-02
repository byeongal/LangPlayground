from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from lang_playground.common.resp import BaseApiResp


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=BaseApiResp(code=exc.status_code, message=str(exc.detail)).dict(),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=BaseApiResp(code=status.HTTP_422_UNPROCESSABLE_ENTITY, message="Validation Error").dict(),
    )


async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=BaseApiResp(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=str(exc)).dict(),
    )


# FIXME: 에러 원인 찾고 수정 필요
def include_exception_handler(app: FastAPI):
    app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
    app.add_exception_handler(Exception, general_exception_handler)
