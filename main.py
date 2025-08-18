import Adafruit_DHT
import time

# Set the sensor type and GPIO pin
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 2  # Change this to the pin where your DHT22 is connected

print("Testing DHT22 sensor...")

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        print(f"Temp={temperature:.1f}°C  Humidity={humidity:.1f}%")
    else:
        print("Failed to retrieve data from DHT22 sensor")

    time.sleep(2)
