import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from gpiozero import Buzzer

GPIO.setmode(GPIO.BCM)

# --- GPIO PINS ---
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 2       # GPIO pin for DHT22 data
LDR_PIN = 22      # GPIO pin connected to LDR digital output
RELAY_PIN = 21    # GPIO pin connected to relay module
Red_led = 3     # GPIO pin connected to White  Led
Green_led = 4     # GPIO pin connected to Green Led
buzzer = Buzzer(20)

# --- GPIO SETUP ---
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(Red_led, GPIO.OUT)
GPIO.setup(Green_led, GPIO.OUT)



print("Starting Smart Environment Monitor...")

try:
    while True:
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
            print("Fan ON (hot temperature)")
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay ON
            GPIO.output(Red_led, GPIO.HIGH)  # Red led On
            GPIO.output(Green_led, GPIO.LOW)  # Green led On
        else:
            print("Fan OFF (cool temperature)")
            GPIO.output(RELAY_PIN, GPIO.LOW)   # relay OFF
            GPIO.output(Green_led, GPIO.HIGH)   # Green led  On
            GPIO.output(Red_led, GPIO.LOW) # Red led OFF
        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting program...")
    GPIO.cleanup()
