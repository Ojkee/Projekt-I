import uvicorn
import os

from backend.rest.router import create_app

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

#STATIC_FILES_DIR = os.path.join(os.getcwd(), "frontend", "dist")


def run_server(port: int, DEV_MODE: bool = False) -> bool:
    app = create_app()

    origins = [
        "https://matika.onrender.com/",
        "http://localhost:5173/",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #if not DEV_MODE:
    #    app.mount(
    #        "/", StaticFiles(directory=STATIC_FILES_DIR, html=True), name="frontend"
    #    )

    PORT = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=False)
