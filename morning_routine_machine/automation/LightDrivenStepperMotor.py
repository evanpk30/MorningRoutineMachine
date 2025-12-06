#!/usr/bin/env python3
import sys
import os
import json
from pathlib import Path
from datetime import datetime, time as dtime

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

from gpiozero import OutputDevice, InputDevice, MotionSensor
import time

from automation.DisplayTempHumLed import temp_hum_disp
from web.logger import log_sensor   # <-- DB logging helper


# ------------------------------
# Config Helpers
# ------------------------------
def load_config():
    """
    Load first-activation settings from instance/config.json
    at the project root.
    """
    project_root = Path(__file__).resolve().parents[1]
    config_path = project_root / "instance" / "config.json"
    default = {
        "first_activation_mode": "light",  # "light" or "time"
        "first_activation_time": "07:30",  # HH:MM 24hr
    }

    try:
        with open(config_path, "r") as f:
            data = json.load(f)
        cfg = default.copy()
        cfg.update(data)
        return cfg
    except (FileNotFoundError, json.JSONDecodeError):
        return default


# ------------------------------
# Stepper Motor Setup
# ------------------------------
motorPins = (18, 25, 24, 23)
motors = [OutputDevice(pin) for pin in motorPins]

CCWStep = (0x01, 0x02, 0x04, 0x08)
CWStep  = (0x08, 0x04, 0x02, 0x01)

def move_one_period(direction, ms):
    """Moves the stepper motor one microstep sequence."""
    steps = CCWStep if direction == 1 else CWStep
    for j in range(4):
        for i in range(4):
            if steps[j] == (1 << i):
                motors[i].on()
            else:
                motors[i].off()
        time.sleep(max(ms, 3) * 0.001)

def move_steps(direction, ms, steps):
    """Move the motor a given number of microsteps."""
    for _ in range(steps):
        move_one_period(direction, ms)

def motor_stop():
    """Turns off all motor outputs."""
    for m in motors:
        m.off()


# ------------------------------
# Motor Rotation Constants
# ------------------------------
FULL_ROTATION_CYCLES = 512
THREE_TURNS = 3 * FULL_ROTATION_CYCLES


# ------------------------------
# Light Sensor Setup (KS0028)
# ------------------------------
LIGHT_PIN = 16
light_sensor = InputDevice(LIGHT_PIN, pull_up=False)

def light_detected():
    """Returns True when the KS0028 detects light."""
    return light_sensor.value == 1


# ------------------------------
# PIR Motion Sensor Setup
# ------------------------------
pir = MotionSensor(21)


# ------------------------------
# State Tracking
# ------------------------------
light_opened_once = False     # First automatic opening happens ONE time
is_open = False               # Current blind state


# ------------------------------
# Main Behavior Loop
# ------------------------------
print("System Ready.")
print("Rule 1: First activation -> OPEN blinds (3 turns)")
print("Rule 2: After that -> Motion toggles OPEN/CLOSE\n")

try:
    while True:
        # Reload config each loop so website changes take effect
        cfg = load_config()
        first_mode = cfg.get("first_activation_mode", "light")
        first_time_str = cfg.get("first_activation_time", "07:30")

        first_time_obj = None
        if first_mode == "time":
            try:
                h, m = map(int, first_time_str.split(":"))
                first_time_obj = dtime(hour=h, minute=m)
            except ValueError:
                first_mode = "light"

        # ======================================================
        # ONE-TIME FIRST ACTIVATION (LIGHT or TIME)
        # ======================================================
        now_time = datetime.now().time()

        if not light_opened_once:
            should_trigger = False
            trigger_reason = ""

            if first_mode == "light":
                if light_detected():
                    should_trigger = True
                    trigger_reason = "Light detected"
            elif first_mode == "time" and first_time_obj is not None:
                # Trigger once when current time is past scheduled time
                if now_time >= first_time_obj:
                    should_trigger = True
                    trigger_reason = f"Scheduled time {first_time_str}"

            if should_trigger:
                # Read and display sensor values
                temp_c, temp_f, humidity = temp_hum_disp()

                # Log values to DB
                log_sensor(
                    temp_c=temp_c,
                    temp_f=temp_f,
                    humidity=humidity,
                    light=light_detected(),
                    motion=False
                )

                print(f"{trigger_reason} -> Opening blinds (3 turns CW)...")
                move_steps(0, 3, THREE_TURNS)
                motor_stop()
                print("Blinds opened from first activation.\n")

                light_opened_once = True
                is_open = True
                time.sleep(1)

        # ======================================================
        # MOTION-BASED TOGGLE
        # ======================================================
        if light_opened_once and pir.motion_detected:

            # Read and display sensor data
            temp_c, temp_f, humidity = temp_hum_disp()

            # Log values to DB
            log_sensor(
                temp_c=temp_c,
                temp_f=temp_f,
                humidity=humidity,
                light=light_detected(),
                motion=True
            )

            print("Motion detected -> Waiting 5 seconds before toggle...")
            time.sleep(5)

            # Toggle blinds
            if is_open:
                print("Closing blinds (3 turns CCW)...")
                move_steps(1, 3, THREE_TURNS)
                is_open = False
            else:
                print("Opening blinds (3 turns CW)...")
                move_steps(0, 3, THREE_TURNS)
                is_open = True

            motor_stop()
            print("Toggle complete.\n")
            time.sleep(1)

        # Reduce CPU load
        time.sleep(0.1)

except KeyboardInterrupt:
    motor_stop()
    print("\nProgram ended safely.")
