from gpiozero import MotionSensor
from signal import pause


pir = MotionSensor(21)
counter = 0

def on_motion():
    global counter
    counter += 1
    print("Motion!", counter)
    
def no_motion():
    print("no one!")
    
pir.when_motion = on_motion
pir.when_no_motion = no_motion

print ("PIR ready")
pause()