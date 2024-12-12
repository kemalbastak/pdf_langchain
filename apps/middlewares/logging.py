from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from apps.es.elasticsearch_logger import logger
import traceback
from apps.utils.exceptions import (BadRequestError, UnauthorizedError, ForbiddenError,
                                   NotFoundError, InternalServerError,
                                   ValidationError, ConflictError, ServiceUnavailableError)
from botocore.exceptions import BotoCoreError, ClientError


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            logger.info(f"Incoming request: {request.method} {request.url} from {request.client.host}")
            response = await call_next(request)
            logger.info(f"Response: {response.status_code} {request.url}")
            return response
        except RequestValidationError as validation_error:
            # Log validation errors
            error_details = {
                "errors": validation_error.errors(),
                "body": await request.body()
            }
            # Capture the function name from the traceback
            error_function = traceback.extract_tb(validation_error.__traceback__)[-1].name
            logger.error(f"Validation error in function {error_function}: {error_details}")
            return JSONResponse(
                status_code=422,
                content={
                    "detail": validation_error.errors()
                }
            )
        except (BadRequestError, UnauthorizedError, ForbiddenError,
                NotFoundError, InternalServerError,
                ValidationError, ConflictError, ServiceUnavailableError) as custom_error:
            # Handle custom errors and log them
            error_function = traceback.extract_tb(custom_error.__traceback__)[-1].name
            logger.error(f"{custom_error.__class__.__name__} in function {error_function}: {custom_error.detail}")
            return JSONResponse(
                status_code=custom_error.status_code,
                content={
                    "detail": custom_error.detail
                }
            )
        except (BotoCoreError, ClientError) as aws_error:
            # Handle AWS-specific errors and log them
            error_function = traceback.extract_tb(aws_error.__traceback__)[-1].name
            logger.error(f"AWS Error in function {error_function}: {aws_error}")
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "An error occurred while interacting with AWS services."
                }
            )
        except Exception as exc:
            # Log general exceptions
            error_trace = traceback.format_exc()
            error_function = traceback.extract_tb(exc.__traceback__)[-1].name
            logger.error(f"Unhandled exception in function {error_function}: {exc} \nTraceback: {error_trace}")
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "An internal server error occurred."
                }
            )