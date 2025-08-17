import adafruit_dht
import board
import time

dht_device = adafruit_dht.DHT22(board.D4)  # Replace D4 with your actual pin

while True:
    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print(f"Temp: {temperature}°C  Humidity: {humidity}%")
    except RuntimeError as e:
        print(f"Error: {e}")
    time.sleep(2)
