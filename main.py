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
            # Control LED based on temperature
            if temp > 29:
                GPIO.output(WHITE_PIN, GPIO.HIGH)   # turn WHITE LED on
                if hum > 70:
                    GPIO.output(GREEN_PIN, GPIO.HIGH)  # turn GREEN LED on
                else:
                    GPIO.output(GREEN_PIN, GPIO.LOW)   # turn GREEN LED off
            else:
                GPIO.output(WHITE_PIN, GPIO.LOW)    # turn WHITE LED off
                GPIO.output(GREEN_PIN, GPIO.LOW)    # make sure GREEN LED is off

        except RuntimeError as e:
            print("Read error:", e)
            # continue after a short delay
        except Exception as e:
            print("Unexpected error:", repr(e))
            break

        time.sleep(2.0)

finally:
    GPIO.cleanup()
