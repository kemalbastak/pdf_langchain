from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, window: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        if client_ip not in self.requests:
            self.requests[client_ip] = []

        self.requests[client_ip] = [timestamp for timestamp in self.requests[client_ip] if
                                    timestamp > current_time - self.window]

        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(status_code=429, content={"message": "Too many requests"})

        self.requests[client_ip].append(current_time)
        return await call_next(request)
