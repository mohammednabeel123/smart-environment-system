import RPi.GPIO as GPIO
import time
import Adafruit_DHT

# --- GPIO SETUP ---
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO pin where DHT22 is connected

LDR_PIN = 17
RELAY_PIN = 27
BUZZER_PIN = 22
BUTTON_PIN = 23
LED1_PIN = 24
LED2_PIN = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED1_PIN, GPIO.OUT)
GPIO.setup(LED2_PIN, GPIO.OUT)

# --- FUNCTIONS ---
def read_dht22():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return humidity, temperature

def button_pressed(channel):
    print("Button pressed → Fan toggled")
    GPIO.output(RELAY_PIN, not GPIO.input(RELAY_PIN))

GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_pressed, bouncetime=300)

# --- MAIN LOOP ---
try:
    while True:
        humidity, temperature = read_dht22()

        if humidity is not None and temperature is not None:
            print(f"Temp: {temperature:.1f}°C  Humidity: {humidity:.1f}%")

            # Fan control
            if temperature > 30:
                GPIO.output(RELAY_PIN, GPIO.HIGH)  # Fan ON
                GPIO.output(LED1_PIN, GPIO.HIGH)   # LED1 ON (fan status)
                print("Fan ON (Temp high)")
            else:
                GPIO.output(RELAY_PIN, GPIO.LOW)   # Fan OFF
                GPIO.output(LED1_PIN, GPIO.LOW)
                print("Fan OFF (Temp normal)")

            # Buzzer control
            if humidity > 70:
                GPIO.output(BUZZER_PIN, GPIO.HIGH)  # Buzzer ON
                GPIO.output(LED2_PIN, GPIO.HIGH)    # LED2 ON (alert)
                print("Buzzer ON (Humidity high)")
            else:
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                GPIO.output(LED2_PIN, GPIO.LOW)
                print("Buzzer OFF (Humidity normal)")

        else:
            print("Failed to read DHT22 sensor")

        # LDR check
        if GPIO.input(LDR_PIN) == 0:
            print("Light detected")
        else:
            print("Darkness detected")

        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    GPIO.cleanup()
