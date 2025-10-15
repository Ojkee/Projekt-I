import uvicorn
import os

from backend.rest.router import create_app

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

STATIC_FILES_DIR = os.path.join(os.getcwd(), "frontend", "dist")

def run_server(port: int, DEV_MODE: bool = False) -> bool:
    app = create_app()

    # Workaround
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if not DEV_MODE:
        app.mount("/", StaticFiles(directory=STATIC_FILES_DIR, html=True), name="frontend")

    uvicorn.run(app, host="localhost", port=port, reload=False)

