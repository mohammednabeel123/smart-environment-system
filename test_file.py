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
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)  # Relay OFF (active-low)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

FAN_TEMP_THRESHOLD = 30  # Relay ON temp

print("Starting Smart Environment Monitor...")
print("Initializing sensors...")
time.sleep(5)  # Wait for sensors to stabilize

try:
    while True:
        # Keep reading until a valid sensor value is obtained
        humidity, temperature = None, None
        while temperature is None or humidity is None:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if temperature is None or humidity is None:
                print("Waiting for valid DHT reading...")
                time.sleep(1)

        # Temperature-based fan control
        if temperature is not None and temperature > FAN_TEMP_THRESHOLD:
            GPIO.output(RELAY_PIN, GPIO.LOW)  # Relay ON (fan ON, active-low)
            buzzer.on()
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}% | Fan ON")
        else:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay OFF (fan OFF, active-low)
            buzzer.off()
            print(f"Temperature: {temperature if temperature is not None else 'N/A'}°C | Humidity: {humidity if humidity is not None else 'N/A'}% | Fan OFF")

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