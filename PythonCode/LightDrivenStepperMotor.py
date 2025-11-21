from gpiozero import OutputDevice, InputDevice, MotionSensor
from DisplayTempHumLed import temp_hum_disp
import time

motorPins = (18, 25, 24, 23)
motors = [OutputDevice(pin) for pin in motorPins]

CCWStep = (0x01, 0x02, 0x04, 0x08)
CWStep  = (0x08, 0x04, 0x02, 0x01)

def move_one_period(direction, ms):
    steps = CCWStep if direction == 1 else CWStep
    for j in range(4):
        for i in range(4):
            if steps[j] == (1 << i):
                motors[i].on()
            else:
                motors[i].off()
        time.sleep(max(ms, 3) * 0.001)

def move_steps(direction, ms, steps):
    for _ in range(steps):
        move_one_period(direction, ms)

def motor_stop():
    for m in motors:
        m.off()

# 3 full rotations → 3 × 512 cycles
FULL_ROTATION_CYCLES = 512
THREE_TURNS = 3 * FULL_ROTATION_CYCLES


# ------------------------------
# Light Sensor Setup (KS0028)
# ------------------------------
LIGHT_PIN = 16
light_sensor = InputDevice(LIGHT_PIN, pull_up=False)

def light_detected():
    return light_sensor.value == 1


# ------------------------------
# PIR Motion Sensor Setup
# ------------------------------
pir = MotionSensor(21)


# ------------------------------
# State Tracking
# ------------------------------
light_opened_once = False   # Has the first "light open" happened?
is_open = False             # Current blinds state


# ------------------------------
# Main Behavior
# ------------------------------
print("System Ready.")
print("First light → OPEN (3 turns)")
print("After that: motion toggles OPEN/CLOSE\n")

try:
    while True:

        # ---------- ONE-TIME LIGHT TRIGGER ----------
        if not light_opened_once and light_detected():
            temp_hum_disp()
            print("Light detected → Opening blinds (3 turns CW)...")
            move_steps(0, 3, THREE_TURNS)
            motor_stop()
            print("Blinds opened from light.\n")

            light_opened_once = True
            is_open = True
            time.sleep(1)

        # ---------- MOTION TOGGLE ----------
        if light_opened_once and pir.motion_detected:
            temp_hum_disp()
            print("Motion detected → waiting 5 seconds before toggle...")
            time.sleep(5)

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

        time.sleep(0.1)

except KeyboardInterrupt:
    motor_stop()
    print("\nProgram ended safely.")
