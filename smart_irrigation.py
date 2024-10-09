import time
import paho.mqtt.client as mqtt
import Adafruit_DHT
import RPi.GPIO as GPIO

# MQTT Settings
broker = 'broker.hivemq.com'
port = 1883
topic = 'smart_irrigation_system/control'
client_id = 'irrigation_client'

# GPIO setup
GPIO.setmode(GPIO.BCM)
pump_pin = 18
GPIO.setup(pump_pin, GPIO.OUT)
GPIO.output(pump_pin, GPIO.LOW)

# Sensor settings
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
soil_moisture_pin = 17
GPIO.setup(soil_moisture_pin, GPIO.IN)

def on_connect(client, userdata, flags, rc):
    client.subscribe(topic)

def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    if message == 'ON':
        GPIO.output(pump_pin, GPIO.HIGH)
    elif message == 'OFF':
        GPIO.output(pump_pin, GPIO.LOW)

client = mqtt.Client(client_id)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)

client.loop_start()

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    soil_moisture = GPIO.input(soil_moisture_pin)

    if soil_moisture == 0:
        GPIO.output(pump_pin, GPIO.HIGH)
    else:
        GPIO.output(pump_pin, GPIO.LOW)

    client.publish(topic, f'Temperature: {temperature}, Humidity: {humidity}, Soil Moisture: {soil_moisture}')
    time.sleep(10)
