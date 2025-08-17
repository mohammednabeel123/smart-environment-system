import RPi.GPIO as GPIO
import time

WHITE_PIN = 3
GREEN_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(WHITE_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(WHITE_PIN, GPIO.HIGH)  # Turn WHITE LED on
        GPIO.output(GREEN_PIN, GPIO.HIGH)  # Turn GREEN LED on
        time.sleep(2)
        GPIO.output(WHITE_PIN, GPIO.LOW)   # Turn WHITE LED off
        GPIO.output(GREEN_PIN, GPIO.LOW)   # Turn GREEN LED off
        time.sleep(2)
finally:
    GPIO.cleanup()
