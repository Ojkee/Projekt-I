import subprocess
import sys
import os
import shutil

BACKEND_DIR = "./backend"
FRONTEND_DIR = "./frontend"
DIST_DIR = os.path.join(FRONTEND_DIR, "dist")

def run_dev():
    print("Running backend server in dev mode...")
    backend_proc = subprocess.Popen(["go", "run", "main.go", "dev"], cwd=BACKEND_DIR)

    print("Running frontend server in dev mode...")
    frontend_proc = subprocess.Popen([r"C:\Program Files\nodejs\npm.cmd", "run", "dev"], cwd=FRONTEND_DIR)

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print("Stopping...")
        backend_proc.terminate()
        frontend_proc.terminate()

def run_prod():
    print("Building frontend...")
    subprocess.run([r"C:\Program Files\nodejs\npm.cmd", "run", "build"], cwd=FRONTEND_DIR, check=True)

    print("Starting backend in production mode...")

    try:
        print("Server is running at http://localhost:8080")
        subprocess.run(["go", "run", "main.go", "prod"], cwd=BACKEND_DIR, check=True)
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
        run_dev()
    elif mode == "prod":
        run_prod()
    else:
        print("Unknwon type: use 'dev' or 'prod'")