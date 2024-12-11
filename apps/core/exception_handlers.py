from typing import List

from fastapi.responses import JSONResponse
from fastapi import Request
from pydantic import BaseModel
from starlette import status


class ValidationErrorModel(BaseModel):
    loc: str
    msg: str


class ValidationErrorResponse(BaseModel):
    detail: List[ValidationErrorModel]


async def validation_exception_handler(
    request: Request, exc: ValidationErrorResponse
) -> JSONResponse:
    custom_error_responses = []
    for error in exc.errors():
        field_name = error["loc"][
            -1
        ]  # Get the last part of the location which is the field name
        custom_error_responses.append(
            {"loc": str(field_name), "msg": str(error["msg"])}
        )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ValidationErrorResponse(detail=custom_error_responses).model_dump(),
    )
