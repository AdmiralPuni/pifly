import paho.mqtt.client as mqtt
from time import sleep

def publish(client, topic, payload):
  client.publish(topic, payload, qos=0)

client = mqtt.Client()

client.connect("34.127.121.177", 1883, 60)
publish(client, "NF1", "delay-22")
sleep(0.3)
