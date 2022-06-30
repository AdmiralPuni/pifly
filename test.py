import paho.mqtt.client as mqtt
import random
from time import sleep

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)

TOPIC_LIST = ["NFFD-BATTERY", "NFFD-WATER", "NFFD-RADAR"]
DEVICE_LIST = ['MONA', 'LISA', 'BOSSA', 'NOVA', 'TERRA', 'COTA']

def publish(client, topic, payload):
  client.publish(topic, payload, qos=0)

while True:
  for topic in TOPIC_LIST:
    for device in DEVICE_LIST:
      payload = random.randint(0, 100)
      publish(client, topic, device + ',' +str(payload))
      sleep(0.5)

  #check for messages
  client.loop(2)

  sleep(1)
