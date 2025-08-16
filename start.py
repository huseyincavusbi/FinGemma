import os
import subprocess
import sys

mode = os.environ.get("APP_MODE", "ui").lower()
port = os.environ.get("PORT", "7860")

if mode == "api":
    cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", port]
else:  # ui
    cmd = [sys.executable, "app/app.py"]

print(f"[start] Mode={mode} -> executing: {' '.join(cmd)}")
subprocess.run(cmd, check=True)
