from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.rest.handlers import run


def create_app() -> FastAPI:
    app = FastAPI(title="Interpreter Service")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(run.router)

    return app

