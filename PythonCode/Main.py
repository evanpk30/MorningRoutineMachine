import time
from LightDrivenStepperMotor import motor_loop_step
from DisplayTempHumLed import temp_hum_disp

def main():
    print("Main system running…")
    blinds_open = False

    while True:
        # 1. Run one logic cycle of motor/light/motion control
    

        # 2. Slow loop slightly so CPU isn't hammered
        time.sleep(0.5)
        

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSystem shutdown.")
