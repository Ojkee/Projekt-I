import uvicorn
import os

from backend.rest.router import create_app

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

STATIC_FILES_DIR = os.path.join(os.getcwd(), "frontend", "dist")

def run_server(port: int, DEV_MODE: bool = False) -> bool:
    app = create_app()

    if not DEV_MODE:
        app.mount("/", StaticFiles(directory=STATIC_FILES_DIR, html=True), name="frontend")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # React dev server
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host="127.0.0.1", port=port, reload=DEV_MODE)

