import time
import threading
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
RELAY_PIN = 16
RED_LED = 3
GREEN_LED = 4
buzzer = Buzzer(20)

# Setup pins
GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.HIGH)  # Relay OFF at start
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

FAN_TEMP_THRESHOLD = 150  # Relay ON temp

# --- Thread functions ---
def ldr_led_control():
    """Thread to control LEDs based on LDR"""
    while True:
        if GPIO.input(LDR_PIN) == 0:  # Light detected
            GPIO.output(RED_LED, GPIO.HIGH)
            GPIO.output(GREEN_LED, GPIO.LOW)
            print("LDR: Light → RED ON, GREEN OFF")
        else:  # Dark
            GPIO.output(RED_LED, GPIO.LOW)
            GPIO.output(GREEN_LED, GPIO.HIGH)
            print("LDR: Dark → RED OFF, GREEN ON")
        time.sleep(0.5)  # fast update for LEDs

def temp_relay_buzzer():
    """Thread to control Relay and Buzzer based on temperature"""
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        if humidity is not None and temperature is not None:
            print(f"Temperature: {temperature:.1f}°C | Humidity: {humidity:.1f}%")
            if temperature >= FAN_TEMP_THRESHOLD:
                GPIO.output(RELAY_PIN, GPIO.LOW)  # Relay ON
                buzzer.on()
                print("Fan ON → Relay + Buzzer")
            else:
                GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay OFF
                buzzer.off()
                print("Fan OFF → Relay + Buzzer")
        else:
            print("Failed to read DHT22")
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Relay OFF
            buzzer.off()

        time.sleep(2)  # slower update for temperature

# --- Start threads ---
try:
    t1 = threading.Thread(target=ldr_led_control, daemon=True)
    t2 = threading.Thread(target=temp_relay_buzzer, daemon=True)
    t1.start()
    t2.start()

    # Keep main thread alive
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting program...")
    buzzer.off()
    GPIO.cleanup()
