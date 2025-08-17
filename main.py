import time
import board
import adafruit_dht
import RPi.GPIO as GPIO


# Setup
GPIO.setmode(GPIO.BCM)
WHITE_PIN = 3
GREEN_PIN = 4
GPIO.setup(WHITE_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

# DHT22
dhtDevice = adafruit_dht.DHT22(board.D2)

try:
    while True:
        try:
            temp = dhtDevice.temperature
            hum = dhtDevice.humidity
            print(f"Temperature: {temp:.1f} °C   Humidity: {hum:.1f}%")

            # Control LED based on temperature
            if temp > 29:
                GPIO.output(WHITE_PIN, GPIO.HIGH)   # turn LED on
                if hum > 72:
                   GPIO.setup(GREEN_PIN, GPIO.HIGH) 
                else:
                    GPIO.setup(GREEN_PIN, GPIO.LOW)       
            else:
                GPIO.output(WHITE_PIN, GPIO.LOW)    # turn LED off

        except RuntimeError as e:
            print("Read error:", e)
            # continue after a short delay
        except Exception as e:
            print("Unexpected error:", repr(e))
            break

        time.sleep(2.0)

finally:
    GPIO.cleanup()
