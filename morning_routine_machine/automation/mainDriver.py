import time
import traceback
import subprocess
import sys

LOG_FILE = "automation.log"
SCRIPT = "LightDrivenStepperMotor.py"

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(msg + "\n")
    print(msg)

if __name__ == "__main__":
    while True:
        try:
            log("Starting automation process...")
            process = subprocess.Popen([sys.executable, SCRIPT])
            process.wait()
            log("Automation script exited unexpectedly.")

        except Exception as e:
            log("Wrapper caught error:\n" + traceback.format_exc())

        log("Restarting in 5 seconds...")
        time.sleep(5)
