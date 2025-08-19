import RPi.GPIO as GPIO
import time

RELAY_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)  # OFF

try:
    while True:
        GPIO.output(RELAY_PIN, GPIO.LOW)   # Should turn fan ON
        time.sleep(2)
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Should turn fan OFF
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
