from fastapi import Request


async def add_custom_headers(request: Request, call_next):
    response = await call_next(request)

    response.headers["X-API-Version"] = "1.0.0"
    response.headers["X-Powered-By"] = "FastAPI"

    return response
