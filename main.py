import Adafruit_DHT
import RPi.GPIO as GPIO
import time

# --- GPIO PINS ---
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 2       # GPIO pin for DHT22 data
LDR_PIN = 22      # GPIO pin connected to LDR digital output
RELAY_PIN = 21    # GPIO pin connected to relay module

# --- GPIO SETUP ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)

print("Starting Smart Environment Monitor...")

try:
    while True:
        # --- Read DHT22 ---
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print(f"Temp: {temperature:.1f}°C  Humidity: {humidity:.1f}%")
        else:
            print("Failed to read from DHT22")

        # --- Read LDR ---
        ldr_value = GPIO.input(LDR_PIN)  # 0 = dark, 1 = light
        if ldr_value == 0:
            print("LDR: Dark")
        else:
            print("LDR: Light detected")

        # --- Fan Control (Relay) ---
        if temperature is not None and temperature > 28:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Fan ON
            print("Fan ON (hot temperature)")
        else:
            GPIO.output(RELAY_PIN, GPIO.LOW)   # Fan OFF
            print("Fan OFF (cool temperature)")

        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting program...")
    GPIO.cleanup()
