import subprocess
import sys
import os
import shutil
import threading

from backend.rest.server import run_server

PORT = 8080

BACKEND_DIR = "./backend"
FRONTEND_DIR = "./frontend"
DIST_DIR = os.path.join(FRONTEND_DIR, "dist")

def install_front_dependencies():
    print("Installing frontend dependencies...")
    subprocess.run(["npm", "install"], cwd=FRONTEND_DIR, check=True)

    # Backend dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", os.path.join(BACKEND_DIR, "requirements.txt")], check=True)

def run_dev():
    print("Starting backend server...")
    threading.Thread(target=run_server, args=(PORT, True), daemon=True).start()

    try:
        subprocess.run(["npm", "run", "dev"], cwd=FRONTEND_DIR, check=True)
    except KeyboardInterrupt:
        print("\nStopping...")

def run_prod():
    print("Building frontend for production...")
    subprocess.run(["npm", "run", "build"], cwd=FRONTEND_DIR, check=True)

    print("Running backend server in production mode...")
    try:
        run_server(PORT, DEV_MODE=False)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if os.path.exists(DIST_DIR):
            print("Removing frontend/dist directory...")
            shutil.rmtree(DIST_DIR)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run.py [dev|prod|install]")
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == "dev":
        run_dev()
    elif mode == "prod":
        run_prod()
    elif mode == "install":
        install_front_dependencies()
    else:
        print("Unknown type: use 'dev', 'prod' or 'install'")
