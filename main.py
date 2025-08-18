import RPi.GPIO as GPIO
import time

RELAY_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

try:
    while True:
        # Turn fan on
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        print("Fan ON")
        time.sleep(5)

        # Turn fan off
        GPIO.output(RELAY_PIN, GPIO.LOW)
        print("Fan OFF")
        time.sleep(5)

finally:
    GPIO.cleanup()
