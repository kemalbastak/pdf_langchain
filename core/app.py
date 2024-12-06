from fastapi.exceptions import RequestValidationError
from core.database import get_db
from core.settings import settings
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import OperationalError
from contextlib import asynccontextmanager
from sqlalchemy.sql import text
from core.exception_handlers import ValidationErrorResponse, validation_exception_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with get_db() as session:
            session.execute(text('SELECT 1'))
            yield
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database connection failed")


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
    exception_handlers={RequestValidationError: validation_exception_handler},
    responses={
        422: {
            "description": "Validation Error",
            "model": ValidationErrorResponse,
        },
    },
)
