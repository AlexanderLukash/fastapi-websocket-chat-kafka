from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Simple FastAPI and Kafka chat",
        description="Fast API for Kafka chat and streaming websocket.",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        debug=True,
    )

    return app
