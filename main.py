import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

# Setup
GPIO.setmode(GPIO.BCM)
WHITE_PIN = 3
GREEN_PIN = 4
DO_PIN = 17  # GPIO pin connected to LDR module digital output

GPIO.setup(WHITE_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(DO_PIN, GPIO.IN)

# DHT22
dhtDevice = adafruit_dht.DHT22(board.D2)

try:
    while True:
        # --- Read temperature and humidity ---
        try:
            temp = dhtDevice.temperature
            hum = dhtDevice.humidity
            print(f"Temperature: {temp:.1f} °C   Humidity: {hum:.1f}%")
            
            # Control LEDs based on temp & humidity
            if temp > 29:
                GPIO.output(WHITE_PIN, GPIO.HIGH)  # WHITE LED on
                if hum < 70:
                    GPIO.output(GREEN_PIN, GPIO.HIGH)  # GREEN LED on
                else:
                    GPIO.output(GREEN_PIN, GPIO.LOW)   # GREEN LED off
            else:
                GPIO.output(WHITE_PIN, GPIO.LOW)      # WHITE LED off
                GPIO.output(GREEN_PIN, GPIO.LOW)      # GREEN LED off

        except RuntimeError as e:
            print("Read error:", e)

        # --- Read LDR digital output ---
        if GPIO.input(DO_PIN):
            print("It's bright!")
        else:
            print("It's dark!")

        time.sleep(2)  # Wait 2 seconds before next reading

finally:
    GPIO.cleanup()
