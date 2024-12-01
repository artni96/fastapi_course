import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

from src.api.routers.auth import user_router  # noqa
from src.api.routers.booking import booking_router  # noqa
from src.api.routers.facilities import facilities_router  # noqa
from src.api.routers.hotels import hotels_router  # noqa
from src.api.routers.rooms import rooms_router  # noqa
from src.config import settings  # noqa
from src.init import redis_manager  # noqa


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()


app = FastAPI(docs_url=None, redoc_url=None, debug=True, lifespan=lifespan)
app.include_router(hotels_router)
app.include_router(user_router)
app.include_router(rooms_router)
app.include_router(booking_router)
app.include_router(facilities_router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url=("https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"),
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url=("https://unpkg.com/redoc@next/bundles/redoc.standalone.js",),
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
