#!/usr/bin/env python3
#############################################################################
# Filename    : DHT11.py
# Description :	read the temperature and humidity data of DHT11
# Author      : freenove
# modification: 2024/07/29
########################################################################
import time
#import only 'datetime'
from datetime import datetime
#import the mysql.connector module
import mysql.connector

import board

#connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="8752Epk0330!",
    database="rasberrypi")

#Check if connection is successful
#Use the is_connected() to see if connection is active
if conn.is_connected():
    print("Connected to MySQL")
    
#Create a cursor object using the connection to execute queries
#A cursor is an object that allows us to execute queries
mycursor = conn.cursor()
    

import adafruit_dht
#initialize the dht sensor object and set it to D4

dhtDevice = adafruit_dht.DHT11(board.D17, use_pulseio=False)

def loop():
    while True:
        try:
            #read temp in celcius from the dht censor
            temp_c = dhtDevice.temperature
            
            #convert to Farenheit
            temp_f = temp_c * (9/5) + 32
            
            #read humidity from dht11
            humidity = dhtDevice.humidity
            
            time.sleep(1)
            
            #print the temp in both F and C
            print("Temperature in Celcius: {:.1f} F | {:.1f} C    Humidity: {}%  Date: {}" .format(temp_f, temp_c, humidity, datetime.now()))
            
            #define the SQL INSERT
            sql = "INSERT INTO TempHum (temp, hum, date_time) VALUES (%s, %s, %s)"
            val = (temp_c, humidity, datetime.now())
            
            #execute SQL statement
            mycursor.execute(sql, val)
            
            #commit the transaction to db
            conn.commit()
            
            #catch RuntimeError, which happens frequently due to sensor read errors
            
        except RuntimeError as error:
            #print the error message then retry
            print(error.args[0])
            time.sleep(2)
            continue #continue after the error is handled, skip the rest of the loop and try again
            
            
            #Catch anyy other unexpected exceptions
        except Exception as error:
            #properly release resources used by the DHT sensor
            dhtDevice.exit()
            #reraise the exception to notify the user of the issue
            time.sleep(2)
        finally:
            dhtDevice.exit()        
            
if __name__ == "__main__":
    print("checking temp")

    try:
        loop()
    except KeyboardInterrupt:
        dhtDevice.exit()
    

