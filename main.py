import Adafruit_DHT
import time

# Set the sensor type and GPIO pin
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 2  # Change this to the pin where your DHT22 is connected
LDR_PIN = 22   # GPIO pin connected to LDR digital output
RELAY_PIN = 21 # GPIO pin connected to Relay

print("Testing DHT22 sensor...")

try:
    while True:
        # Read DHT22
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            print(f"Temp: {temperature:.1f}C  Humidity: {humidity:.1f}%")
        else:
            print("Failed to read from DHT22")

        # Read LDR
        ldr_value = GPIO.input(LDR_PIN)  # 0 = dark, 1 = light (depends on module)
        if ldr_value == 0:
            print("LDR: Dark")
        else:
            print("LDR: Light detected")

        # Control fan with relay (example logic)
        if temperature is not None and temperature > 28:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn fan ON
            print("Fan ON (hot temperature)")
        else:
            GPIO.output(RELAY_PIN, GPIO.LOW)   # Turn fan OFF
            print("Fan OFF (cool temperature)")

        time.sleep(2)

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
