# Smart Environment Monitor 🌡️💡

## **Project Overview**

This project is a **portable Smart Environment Monitor** built with a Raspberry Pi. It automatically monitors **temperature, humidity, and light levels** and controls a **fan, buzzer, and LEDs** accordingly. The system is powered by a **battery + boost converter**, making it fully portable and reliable.

---

## **Features**

* **Temperature & Humidity Monitoring:** Uses **DHT22 sensor** to read environmental conditions.
* **Automatic Fan & Buzzer Control:** Fan and buzzer activate when the temperature exceeds a set threshold.
* **Light Detection:** Uses an **LDR** to detect light/dark conditions. Red and green LEDs respond in real-time.
* **Portable Power:** Battery + boost converter provides stable power for anywhere operation.
* **Threaded Operation:** LDR LEDs and temperature control run independently for fast, simultaneous response.

---

## **Components**

* Raspberry Pi (any model with GPIO pins)
* DHT22 Temperature & Humidity Sensor
* LDR (Light Dependent Resistor)
* 1-Channel Relay Module
* Fan
* Buzzer
* Red & Green LEDs
* Battery + Boost Converter
* Jumper wires, breadboard, resistors

---

## **Wiring & Connections**

**DHT22 → Relay + Fan + Buzzer**

* DHT22 Data → GPIO2 (10kΩ pull-up to VCC)
* Relay IN → GPIO16
* Relay COM → Fan positive
* Buzzer → GPIO20

**LDR → LEDs**

* LDR → GPIO22
* Red LED → GPIO3
* Green LED → GPIO4

**Power:**

* Battery → Boost Converter → Raspberry Pi + peripherals

---

## **Software**

* Written in **Python 3**
* Uses libraries: `RPi.GPIO`, `gpiozero`, `Adafruit_DHT`, `threading`
* **Threaded design** allows LDR LEDs and temperature-controlled relay/buzzer to operate independently.

---

## **Usage**

1. Clone the repository:

```bash
git clone [your GitHub link]
```

2. Install dependencies:

```bash
pip3 install RPi.GPIO gpiozero Adafruit_DHT
```

3. Run the program:

```bash
python3 main.py
```

4. Watch LEDs respond to light and the fan/buzzer respond to temperature.

---

## **Notes / Troubleshooting**

* Ensure **DHT22 has a 10kΩ pull-up resistor** to VCC.
* Use **stable power** for Raspberry Pi and peripherals.
* Relay is **active LOW**: `GPIO.LOW = ON`, `GPIO.HIGH = OFF`.
* Some initial readings from DHT22 may be `None` — the program includes a **sanity check** to skip invalid values.

---

## **Future Improvements**

* Add a **manual button override** for fan control.
* Log temperature, humidity, and light data to **CSV or database**.
* Build a **web dashboard** to visualize sensor data in real-time.

