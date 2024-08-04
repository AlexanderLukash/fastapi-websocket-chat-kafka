from contextlib import asynccontextmanager

from fastapi import FastAPI

from aiojobs import Scheduler
from punq import Container

from app.application.api.lifespan import (
    close_message_broker,
    consume_in_background,
    init_message_broker,
)
from app.logic.init import init_container
from app.application.api.v1.urls import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()

    container: Container = init_container()
    scheduler: Scheduler = container.resolve(Scheduler)

    job = await scheduler.spawn(consume_in_background())

    yield
    await close_message_broker()
    await job.close()


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
