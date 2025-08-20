import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from gpiozero import Buzzer
from gpiozero import Button

# --- GPIO SETUP ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Sensors
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 2
LDR_PIN = 22
RELAY_PIN = 16

# Actuators
RED_LED = 3
GREEN_LED = 4
buzzer = Buzzer(20)
button = Button(17, pull_up=False)

# Setup GPIO pins
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)  # Relay OFF at start
GPIO.output(RELAY_PIN, GPIO.HIGH)                   # Force OFF
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

FAN_TEMP_THRESHOLD = 30  # Relay ON temp

print("Starting Smart Environment Monitor...")

try:
    while True:
        # Read DHT22 sensor
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        # Skip iteration if sensor reading failed
        if temperature is None or humidity is None:
            print("Waiting for DHT sensor...")
            time.sleep(2)
            continue

        # Temperature-based fan control
        if temperature > FAN_TEMP_THRESHOLD:
            GPIO.output(RELAY_PIN, GPIO.LOW)   # Relay ON (fan ON)
            buzzer.on()
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}% | Fan ON")
        else:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay OFF (fan OFF)
            buzzer.off()
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}% | Fan OFF")

        # LDR-based LED control
        if GPIO.input(LDR_PIN) == 0:  # Light detected
            GPIO.output(RED_LED, GPIO.HIGH)
            GPIO.output(GREEN_LED, GPIO.LOW)
            print("LDR: Light detected")
        else:  # Dark
            GPIO.output(RED_LED, GPIO.LOW)
            GPIO.output(GREEN_LED, GPIO.HIGH)
            print("LDR: Dark")

        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting program...")
    buzzer.off()
    GPIO.cleanup()
