import time
import board
import adafruit_dht
import RPi.GPIO as GPIO


# Setup
GPIO.setmode(GPIO.BCM)
LED_PIN = 3
GPIO.setup(LED_PIN, GPIO.OUT)

# DHT22
dhtDevice = adafruit_dht.DHT22(board.D2)

try:
    while True:
        try:
            temp = dhtDevice.temperature
            hum = dhtDevice.humidity
            print(f"Temperature: {temp:.1f} °C   Humidity: {hum:.1f}%")

            # Control LED based on temperature
            if temp < 28:
                GPIO.output(LED_PIN, GPIO.HIGH)   # turn LED on
            else:
                GPIO.output(LED_PIN, GPIO.LOW)    # turn LED off

        except RuntimeError as e:
            print("Read error:", e)
            # continue after a short delay
        except Exception as e:
            print("Unexpected error:", repr(e))
            break

        time.sleep(2.0)

finally:
    GPIO.cleanup()
