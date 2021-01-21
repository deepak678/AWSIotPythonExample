# Import package
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import ssl
import time

# Define Variables
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
sensor = 16
led = 18

#setup GPIO mode
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(led,GPIO.OUT)

MQTT_HOST = "a2zxp1r0bqioas-ats.iot.us-east-2.amazonaws.com"
CA_ROOT_CERT_FILE = "./cert/root-CA.crt"
THING_CERT_FILE = "./cert/MyThing.cert.pem"
THING_PRIVATE_KEY = "./cert/MyThing.private.key"

# Define on_publish event function
def on_publish(client, userdata, mid):
        print("Message Published...")

#define on connect event function
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

# Initiate MQTT Client
client = mqtt.Client()

# Register publish callback function
client.on_publish = on_publish

#register connect callback function
client.on_connect = on_connect

# Configure TLS Set
client.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

# Connect with MQTT Broker
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
client.loop_start()

try:
   count = 0
   while True:
      if GPIO.input(sensor):
          count = count + 1
          print("object Detected",count)
          client.publish('test/testing',payload = 'Object Detected' + str(count),qos=1)
          GPIO.output(led, GPIO.HIGH)
          while GPIO.input(sensor):
              time.sleep(0.2)
      else:
        GPIO.output(led, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exception Occured")

# Disconnect from MQTT_Broker
# client.disconnect()
