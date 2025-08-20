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
button = Button(17,pull_up = False)

# --- GPIO SETUP ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)  # Relay OFF at start
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)


FAN_TEMP_THRESHOLD = 30  # Relay ON temp


print("Starting Smart Environment Monitor...")
try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        # Temperature-based fan control
        if temperature < FAN_TEMP_THRESHOLD:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay OFF
            buzzer.off()
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}% | Fan OFF")
        else:
            GPIO.output(RELAY_PIN, GPIO.LOW)   # Relay ON
            buzzer.on()
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}% | Fan ON")

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
