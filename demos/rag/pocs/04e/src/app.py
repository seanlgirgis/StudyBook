from __future__ import annotations

from fastapi import FastAPI

try:
    from .routes import router
except ImportError:  # pragma: no cover
    from routes import router


def create_app() -> FastAPI:
    app = FastAPI(title="POC 04e RAG Service Layer", version="0.1.0")
    app.include_router(router, prefix="/v1")
    return app


app = create_app()
