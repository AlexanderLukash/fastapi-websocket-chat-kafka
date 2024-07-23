from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.application.api.lifespan import (
    close_kafka,
    start_kafka,
)
from app.application.api.v1.urls import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_kafka()
    yield
    await close_kafka()


def create_app():
    app = FastAPI(
        title="Simple Kafka Chat",
        docs_url="/api/docs",
        description="A simple kafka + ddd example.",
        debug=True,
        lifespan=lifespan,
    )
    app.include_router(v1_router, prefix="/api")

    return app
