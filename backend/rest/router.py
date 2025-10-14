from fastapi import FastAPI
from backend.rest.handlers import run

def create_app() -> FastAPI:
    app = FastAPI(title="Interpreter Service")

    app.include_router(run.router)
    return app