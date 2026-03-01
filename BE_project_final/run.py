"""
Start the Industrial Safety Monitoring System.
Run:  python run.py
"""

import os
import subprocess
import sys
import platform

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IS_WIN   = platform.system() == "Windows"
UVICORN  = os.path.join(BASE_DIR, "venv", "Scripts" if IS_WIN else "bin", "uvicorn")

# Fall back to system uvicorn if venv not found
if not os.path.exists(UVICORN):
    UVICORN = "uvicorn"

env_file = os.path.join(BASE_DIR, ".env")
if not os.path.exists(env_file):
    print("⚠  .env file not found. Run  python setup.py  first.")
    sys.exit(1)

# Load PORT from .env if present
port = "8000"
with open(env_file) as f:
    for line in f:
        if line.startswith("APP_PORT="):
            port = line.strip().split("=", 1)[1]
            break

print("🚀  Starting Industrial Safety Monitoring System …")
print(f"    Dashboard → http://localhost:{port}")
print(f"    API Docs  → http://localhost:{port}/docs")
print("    Press Ctrl+C to stop.\n")

subprocess.run(
    [UVICORN, "app.main:app", "--reload", "--host", "0.0.0.0", "--port", port],
    cwd=BASE_DIR,
)
