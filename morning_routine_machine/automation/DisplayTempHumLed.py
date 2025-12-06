#!/usr/bin/env python3
import time
from automation.LCDDisplay import CharLCD1602
from automation.dht_reader import read_dht   # 👈 IMPORT YOUR DHT FUNCTION

lcd1602 = CharLCD1602()


def temp_hum_disp():
    lcd1602.init_lcd(addr=None, bl=1)
    lcd1602.clear()

    temp_c, temp_f, humidity = read_dht()

    # If sensor failed this cycle, just skip displaying bad data
    if temp_c is None:
        time.sleep(2)
        return None, None, None   # <--- important fix

    lcd1602.clear()

    line1 = "T:{:.1f}F {:.1f}C".format(temp_f, temp_c)
    lcd1602.write(0, 0, line1[:16])

    line2 = "Humidity: {}%".format(humidity)
    lcd1602.write(0, 1, line2[:16])

    return temp_c, temp_f, humidity   # <-- MUST RETURN


def destroy():
    lcd1602.clear()

if __name__ == '__main__':
    print('Program is starting ... ')
    try:
        temp_hum_disp()
    except KeyboardInterrupt:
        destroy()
        print("Program stopped.")
