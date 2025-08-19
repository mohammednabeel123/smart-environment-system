import RPi.GPIO as GPIO
import time

RELAY_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)  # OFF

try:
    while True:
        print("Relay ON")
        GPIO.output(RELAY_PIN, GPIO.LOW)   # ON
        time.sleep(2)
        print("Relay OFF")
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # OFF
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
