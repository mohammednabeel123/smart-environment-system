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

# Ensure all outputs are in a safe state initially
GPIO.output(RELAY_PIN, GPIO.HIGH)  # Ensure relay is OFF
GPIO.output(RED_LED, GPIO.LOW)
GPIO.output(GREEN_LED, GPIO.LOW)
buzzer.off()

print("Starting Smart Environment Monitor...")
print("Initializing sensors...")
time.sleep(5)  # Wait for sensors to stabilize

# Function to read DHT sensor with better error handling
def read_dht_sensor():
    try:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN, retries=5, delay_seconds=1)
        return humidity, temperature
    except Exception as e:
        print(f"Error reading DHT sensor: {e}")
        return None, None

try:
    # Read initial temperature to check if it's valid
    humidity, temperature = read_dht_sensor()
    
    if temperature is None:
        print("Failed to get temperature reading. Please check DHT sensor connection.")
    else:
        print(f"Initial temperature reading: {temperature:.1f}°C")
        print(f"Temperature threshold for fan: {FAN_TEMP_THRESHOLD}°C")
    
    while True:
        humidity, temperature = read_dht_sensor()
        
        # If we can't get a reading, skip this iteration
        if temperature is None or humidity is None:
            print("Failed to get sensor reading. Skipping...")
            time.sleep(2)
            continue

        # Temperature-based fan control
        if temperature > FAN_TEMP_THRESHOLD:
            GPIO.output(RELAY_PIN, GPIO.LOW)  # Relay ON (fan ON, active-low)
            buzzer.on()
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}% | Fan ON")
        else:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay OFF (fan OFF, active-low)
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
    # Ensure all outputs are turned off on exit
    buzzer.off()
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    GPIO.output(RED_LED, GPIO.LOW)
    GPIO.output(GREEN_LED, GPIO.LOW)
    GPIO.cleanup()