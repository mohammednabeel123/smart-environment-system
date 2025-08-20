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
# Initialize pins
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)  # Relay OFF at start
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

FAN_TEMP_THRESHOLD = 30  # Relay ON temp


print("Starting Smart Environment Monitor...")

try:
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if temperature < FAN_TEMP_THRESHOLD:
            GPIO.setup(RELAY_PIN, GPIO.LOW)
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}%")
            print("pressed")
            buzzer.off() 
        else:
            GPIO.setup(RELAY_PIN, GPIO.HIGH)
            print("Button not pressed")
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}%")
            print("Fan ON (Relay + Buzzer)")
            print(f"Temperature raw value: {repr(temperature)}, type: {type(temperature)}")
            buzzer.on()
        
        if GPIO.input(LDR_PIN) == 0:  # Light detected
            print("LDR: Light detected")
            GPIO.output(RED_LED, GPIO.HIGH)
            GPIO.output(GREEN_LED, GPIO.LOW)
        else:  # Dark
            print("LDR: Dark")
            GPIO.output(RED_LED, GPIO.LOW)
            GPIO.output(GREEN_LED, GPIO.HIGH)
        
    time.sleep(2)

except KeyboardInterrupt:
    print("Exiting program...")
    buzzer.off()
    GPIO.cleanup()