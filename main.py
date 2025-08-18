import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from gpiozero import Buzzer

# ----------------------------
# GPIO PIN SETUP
# ----------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Sensors
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 2       # DHT22 data pin
LDR_PIN = 22      # LDR digital output

# Actuators / Indicators
RELAY_PIN = 21    # Relay (simulating fan)
RED_LED = 3       # Red LED = Fan ON
GREEN_LED = 4     # Green LED = Fan OFF / Safe
BUZZER_PIN = 20
buzzer = Buzzer(BUZZER_PIN)

# Initialize pins
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

# ----------------------------
# MAIN LOOP
# ----------------------------

print("Starting Smart Environment Monitor...")
try:
    while True:
        # --- Read DHT22 ---
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}%")
        else:
            print("Failed to read from DHT22 sensor")

        # --- Read LDR ---
        if GPIO.input(LDR_PIN) == 0:
            print("LDR: Dark")
        else:
            print("LDR: Light detected")

        # --- Temperature Logic (Threshold 30°C) ---
        if temperature is not None and temperature >= 30:
            print("Fan ON (Red LED + Relay + Buzzer)")
            GPIO.output(RELAY_PIN, GPIO.HIGH)    # Relay ON
            GPIO.output(RED_LED, GPIO.HIGH)      # Red LED ON
            GPIO.output(GREEN_LED, GPIO.LOW)     # Green LED OFF
            buzzer.on()                          # Buzzer ON
        else:
            print("Fan OFF (Green LED)")
            GPIO.output(RELAY_PIN, GPIO.LOW)     # Relay OFF
            GPIO.output(RED_LED, GPIO.LOW)       # Red LED OFF
            GPIO.output(GREEN_LED, GPIO.HIGH)    # Green LED ON
            buzzer.off()                         # Buzzer OFF

        time.sleep(2)  # Delay before next reading

except KeyboardInterrupt:
    print("Exiting program...")
    buzzer.off()
    GPIO.cleanup()
