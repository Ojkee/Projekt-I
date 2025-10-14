from backend.rest.server import run_server

import subprocess
import sys
import os
import shutil

BACKEND_DIR = "./backend"
FRONTEND_DIR = "./frontend"
DIST_DIR = os.path.join(FRONTEND_DIR, "dist")

DEV_PORT = 5173
PROD_PORT = 8080

def install_dependencies():
    print("Installing frontend dependencies...")
    subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)

def run_prod():
    install_dependencies()
    print("Building frontend...")
    subprocess.run(["npm", "run", "build"], cwd=FRONTEND_DIR, check=True)

    print("Running backend server in production mode...")

    try:
        print("Server is running at http://localhost:{}".format(PROD_PORT))
        run_server(PROD_PORT, DEV_MODE=False)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if os.path.exists(DIST_DIR):
            print("Removing frontend/dist directory...")
            shutil.rmtree(DIST_DIR)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run.py [dev|prod]")
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == "dev":
        pass
    elif mode == "prod":
        run_prod()
    else:
        print("Unknwon type: use 'dev' or 'prod'")