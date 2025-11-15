from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.rest.handlers import run
from backend.rest.handlers import formula_list_api


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
    app.include_router(formula_list_api.router)

    return app
