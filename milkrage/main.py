from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from uvicorn import run

from milkrage.config import Config
from milkrage.routers.home import router as home_router
from milkrage.routers.posts import router as posts_router
from milkrage.routers.tags import router as tags_router


def create_app() -> FastAPI:
    config = Config()
    app = FastAPI()
    static = StaticFiles(directory=config.static_path)

    app.include_router(home_router)
    app.include_router(posts_router, prefix="/posts")
    app.include_router(tags_router, prefix="/tags")

    app.mount("/static", static, name="static")

    # Documentation is disabled because used Jinja template engine.
    app.docs_url = None
    app.redoc_url = None

    return app


if __name__ == "__main__":
    # Development only
    run(create_app(), host="127.0.0.1", port=5001)
