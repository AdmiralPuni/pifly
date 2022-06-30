import paho.mqtt.client as mqtt
import random
from time import sleep

client = mqtt.Client()
client.connect("broker.hivemq.com", 1883, 60)

TOPIC_LIST = ["NFFD-BATTERY", "NFFD-WATER", "NFFD-RADAR"]
DEVICE_LIST = ['MONA', 'LISA', 'BOSSA', 'NOVA', 'TERRA', 'COTA']

def publish(client, topic, payload):
  client.publish(topic, payload, qos=0)

loop_count = 0

while True:
  loop_count += 1
  for topic in TOPIC_LIST:
    #only send battery
    if topic != "NFFD-BATTERY":
      continue
    for device in DEVICE_LIST:
      

      print("Publishing to topic: " + topic + " device: " + device)
      payload = random.randint(0, 100)
      publish(client, topic, device + ',' +str(payload))
      sleep(1.5)
    #randomly sleep between 1-3 seconds
    #sleep(5)

  #check for messages
  #client.loop(2)
  print("Loop count: " + str(loop_count))
  sleep(1)
