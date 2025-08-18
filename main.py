import RPi.GPIO as GPIO
import time

# Setup
RELAY_PIN = 21 # change to the GPIO pin connected to your relay
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

try:
    while True:
        print("Relay ON")
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # turns relay ON
        time.sleep(5)

        print("Relay OFF")
        GPIO.output(RELAY_PIN, GPIO.LOW)   # turns relay OFF
        time.sleep(5)

finally:
    GPIO.cleanup()
