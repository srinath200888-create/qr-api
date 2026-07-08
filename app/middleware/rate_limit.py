import time
import json
from collections import defaultdict
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests: dict[str, list[float]] = defaultdict(list)
        self.tier_limits = {
            "free": 3000,
            "basic": 50000,
            "pro": 300000,
            "ultra": 1000000,
        }

    def get_tier(self, api_key: str) -> str:
        return "free"

    async def dispatch(self, request: Request, call_next):
        if not settings.rate_limit_enabled:
            return await call_next(request)

        rapidapi_key = request.headers.get("X-RapidAPI-Key")
        if rapidapi_key and settings.rapidapi_enabled:
            return await call_next(request)

        api_key = rapidapi_key or request.client.host if request.client else "unknown"
        tier = self.get_tier(api_key)
        limit = self.tier_limits.get(tier, 3000)

        now = time.time()
        day_ago = now - 86400
        self.requests[api_key] = [t for t in self.requests[api_key] if t > day_ago]

        if len(self.requests[api_key]) >= limit:
            return Response(
                content=json.dumps({"success": False, "error": "rate_limit_exceeded"}),
                status_code=429,
                media_type="application/json",
            )

        self.requests[api_key].append(now)
        return await call_next(request)
