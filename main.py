import RPi.GPIO as GPIO
import time

WHITE_PIN = 3
GREEN_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(WHITE_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

try:
    GPIO.output(WHITE_PIN, GPIO.HIGH)  # Turn WHITE LED on
    GPIO.output(GREEN_PIN, GPIO.HIGH)  # Turn GREEN LED on
    time.sleep(5)                       # Wait 5 seconds
finally:
    GPIO.cleanup()
