import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

# --- GPIO Pins ---
WHITE_PIN = 17  # Changed to avoid conflicts with I2C
GREEN_PIN = 27
DO_PIN = 22      # LDR digital output

# --- Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(WHITE_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(DO_PIN, GPIO.IN)

# --- DHT22 Setup ---
dhtDevice = adafruit_dht.DHT22(board.D4)  # Use a free GPIO pin

try:
    while True:
        # --- Read temperature and humidity ---
        try:
            temp = dhtDevice.temperature
            hum = dhtDevice.humidity
            print(f"Temperature: {temp:.1f} °C   Humidity: {hum:.1f}%")
            
            # Control LEDs based on temperature & humidity
            if temp > 29:
                GPIO.output(WHITE_PIN, GPIO.HIGH)
                if hum < 70:
                    GPIO.output(GREEN_PIN, GPIO.HIGH)
                else:
                    GPIO.output(GREEN_PIN, GPIO.LOW)
            else:
                GPIO.output(WHITE_PIN, GPIO.LOW)
                GPIO.output(GREEN_PIN, GPIO.LOW)

        except RuntimeError as e:
            print("DHT Read error:", e)
        except Exception as e:
            print("Unexpected error:", repr(e))
            break

        # --- Read LDR digital output ---
        if GPIO.input(DO_PIN):
            print("It's bright!")
        else:
            print("It's dark!")

        time.sleep(2)  # Wait 2 seconds before next reading

finally:
    GPIO.cleanup()
