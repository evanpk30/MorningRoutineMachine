import time

import board

import adafruit_dht

dhtDevice = adafruit_dht.DHT11(board.D17)

def loop():
    while True:
        try:  
            temp_c = dhtDevice.temperature
            
            humidity = dhtDevice.humidity
            
            temp_f = temp_c * (9/5) + 32
            
            print("Temp C: {:.1f}, Temp F: {:.1f}, Humidity: {:.1f}" .format(temp_c, temp_f, humidity))
            
            time.sleep(1)
            
        finally:
            dhtDevice.exit()
            
