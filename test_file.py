import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from gpiozero import Buzzer import Button

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
button = Button(17)
# Initialize pins
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)  # Relay OFF at start
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)


while True:
    if button.is_pressed:
        print("pressed")
    else:
        print("Button not pressed")
        