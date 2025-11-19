from gpiozero import InputDevice
import time

PIN = 16            # KS0028 D0 pin (BCM numbering)
sensor = InputDevice(PIN, pull_up=False)

SAMPLE_RATE = 400   # samples per second
WINDOW_SEC   = 0.5  # averaging window
SAMPLES = int(SAMPLE_RATE * WINDOW_SEC)

ALPHA = 0.25        # smoothing factor for EMA
ema = None

print(f"KS0028 digital light sensor on BCM {PIN}")
print("Press Ctrl+C to stop.")

try:
    while True:
        highs = 0
        for _ in range(SAMPLES):
            if sensor.value:
                highs += 1
            time.sleep(1 / SAMPLE_RATE)
        pct = 100.0 * highs / SAMPLES
        ema = pct if ema is None else (ALPHA * pct + (1 - ALPHA) * ema)
        print(f"Instant={pct:5.1f}%  Smoothed={ema:5.1f}%")
except KeyboardInterrupt:
    pass
