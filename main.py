import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from gpiozero import Buzzer

# --- GPIO SETUP ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Sensors
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 2
LDR_PIN = 22

# Actuators
RELAY_PIN = 21
RED_LED = 3
GREEN_LED = 4
buzzer = Buzzer(20)

# Initialize pins
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

FAN_TEMP_THRESHOLD = 30  # Relay ON temp


print("Starting Smart Environment Monitor...")

try:
    while True:
        # --- Read DHT22 ---
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        temperature = float(temperature)
        if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}%")
        else:
            print("Failed to read from DHT22 sensor")
            time.sleep(2)
            continue

        # --- LDR LED control ---
        if GPIO.input(LDR_PIN) == 0:  # Light detected
            print("LDR: Light detected")
            GPIO.output(RED_LED, GPIO.HIGH)
            GPIO.output(GREEN_LED, GPIO.LOW)
        else:  # Dark
            print("LDR: Dark")
            GPIO.output(RED_LED, GPIO.LOW)
            GPIO.output(GREEN_LED, GPIO.HIGH)

        # --- Temperature relay/fan control ---
        if temperature >= FAN_TEMP_THRESHOLD:
            print("Fan ON (Relay + Buzzer)")
            print(f"Temperature raw value: {repr(temperature)}, type: {type(temperature)}")
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            buzzer.on()
        else:
            print("Fan OFF (Relay + Buzzer)")
            GPIO.output(RELAY_PIN, GPIO.LOW)
            buzzer.off()

        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting program...")
    buzzer.off()
    GPIO.cleanup()
