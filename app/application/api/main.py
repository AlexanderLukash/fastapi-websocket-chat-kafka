from fastapi import FastAPI

from app.application.api.v1.urls import router as v1_router


def create_app():
    app = FastAPI(
        title="Simple Kafka Chat",
        docs_url="/api/docs",
        description="A simple kafka + ddd example.",
        debug=True,
    )
    app.include_router(v1_router, prefix="/api")
    return app
