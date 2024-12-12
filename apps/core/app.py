from fastapi.exceptions import RequestValidationError
from apps.core.database import sessionmanager
from apps.core.settings import settings
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import OperationalError
from contextlib import asynccontextmanager
from sqlalchemy.sql import text
from apps.middlewares.rate_limiter import RateLimitMiddleware
from apps.api import pdf_router, chat_router
from apps.middlewares.logging import LoggingMiddleware

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
)

app.include_router(pdf_router)
app.include_router(chat_router)
app.add_middleware(LoggingMiddleware)


app.add_middleware(RateLimitMiddleware, max_requests=50, window=60)
