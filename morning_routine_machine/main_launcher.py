#!/usr/bin/env python3
import subprocess
import sys
import time
import threading
import traceback
from pathlib import Path

# Base directory of this project (where main_launcher.py lives)
BASE_DIR = Path(__file__).resolve().parent

LOG_FILE = BASE_DIR / "automation.log"
AUTOMATION_SCRIPT = BASE_DIR / "automation" / "LightDrivenStepperMotor.py"


def log(msg: str):
    """Simple logger to both console and file."""
    line = f"[AUTOMATION] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except Exception:
        # Don't crash if logging fails
        pass


def run_automation_loop():
    """
    Run the automation script in a loop as a separate process.
    If it exits, wait 5 seconds and restart.
    """
    while True:
        try:
            log(f"Starting automation script: {AUTOMATION_SCRIPT}")
            process = subprocess.Popen(
                [sys.executable, str(AUTOMATION_SCRIPT)],
                cwd=str(BASE_DIR / "automation"),   # run it from /automation
            )
            ret = process.wait()
            log(f"Automation script exited with code {ret}. Restarting in 5 seconds...")
        except Exception:
            log("Wrapper caught error:\n" + traceback.format_exc())

        time.sleep(5)


def run_flask():
    """
    Import and run your Flask app from web/app.py
    """
    # Make sure BASE_DIR is on sys.path so 'web' package can be imported
    if str(BASE_DIR) not in sys.path:
        sys.path.insert(0, str(BASE_DIR))

    # Import app from web/app.py (where you have: app = Flask(__name__))
    from web.app import app

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True,
    )


if __name__ == "__main__":
    # Start automation in background thread
    automation_thread = threading.Thread(
        target=run_automation_loop,
        daemon=True,
    )
    automation_thread.start()

    # Run Flask in the main thread
    run_flask()
