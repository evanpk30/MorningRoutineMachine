#!/usr/bin/env python3
import time
from LCDDisplay import CharLCD1602
from dht_reader import read_dht   # 👈 IMPORT YOUR DHT FUNCTION

lcd1602 = CharLCD1602()  

def loop():
    while True:
        temp_c, temp_f, humidity = read_dht()

        # If sensor failed this cycle, just skip displaying bad data
        if temp_c is None:
            time.sleep(2)
            continue

        lcd1602.clear()

        # Line 1: temperature in F and C (truncate to 16 chars)
        line1 = "T:{:.1f}F {:.1f}C".format(temp_f, temp_c)
        lcd1602.write(0, 0, line1[:16])

        # Line 2: humidity
        line2 = "Humidity: {}%".format(humidity)
        lcd1602.write(0, 1, line2[:16])

        time.sleep(2)   # update every 2 seconds

def destroy():
    lcd1602.clear()

if __name__ == '__main__':
    print('Program is starting ... ')
    lcd1602.init_lcd(addr=None, bl=1)
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
        print("Program stopped.")
