from fastapi.exceptions import RequestValidationError
from apps.core.database import sessionmanager
from apps.core.settings import settings
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import OperationalError
from contextlib import asynccontextmanager
from sqlalchemy.sql import text
from apps.core.exception_handlers import (
    ValidationErrorResponse,
    validation_exception_handler,
)
from apps.middlewares.rate_limiter import RateLimitMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with sessionmanager.connect() as session:
            # Test the database connection
            await session.execute(text("SELECT 1"))
        yield
        if sessionmanager._engine is not None:
            # Close the DB connection
            await sessionmanager.close()
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

app.add_middleware(RateLimitMiddleware, max_requests=50, window=60)


