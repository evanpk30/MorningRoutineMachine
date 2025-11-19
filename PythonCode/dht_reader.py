import time
import board
import adafruit_dht

# initialize the dht sensor object and set it to D17
dhtDevice = adafruit_dht.DHT11(board.D17, use_pulseio=False)

def read_dht():
    """
    Try to read from the DHT11 once.
    Returns (temp_c, temp_f, humidity) or (None, None, None) on error.
    """
    try:
        temp_c = dhtDevice.temperature
        humidity = dhtDevice.humidity

        if temp_c is None or humidity is None:
            # sensor sometimes gives None
            raise RuntimeError("Sensor returned None")

        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f, humidity

    except RuntimeError as error:
        # This happens a lot with DHT sensors, we just retry later
        print("DHT read error:", error.args[0])
        return None, None, None

    except Exception as error:
        print("Unexpected DHT error:", error)
        # Only exit sensor on truly fatal errors
        dhtDevice.exit()
        raise

# Optional: keep your old standalone loop for testing
if __name__ == "__main__":
    print("checking temp")
    try:
        while True:
            temp_c, temp_f, humidity = read_dht()
            if temp_c is not None:
                print(
                    "Temperature: {:.1f} F | {:.1f} C    Humidity: {}%".format(
                        temp_f, temp_c, humidity
                    )
                )
            time.sleep(2)
    except KeyboardInterrupt:
        dhtDevice.exit()
        print("Stopped.")
