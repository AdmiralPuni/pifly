import paho.mqtt.client as mqtt
import random
from time import sleep

def publish(client, topic, payload):
    client.publish(topic, payload, qos=0)

client = mqtt.Client()
client.publish("A-battery", "20")

client.connect("34.127.121.177", 1883, 60)

max_battery_value = [90, 70, 10]
current_battery = [90, 70, 60]

max_water_value = [100, 70, 80]
current_water = [100, 70, 80]

while True:
  publish(client, "A-battery", current_battery[0])
  publish(client, "B-battery", current_battery[1])
  publish(client, "C-battery", current_battery[2])
  publish(client, "A-water_level", current_water[0])
  publish(client, "B-water_level", current_water[1])
  publish(client, "C-water_level", current_water[2])
  publish(client, "NF1", 22)

  for i in range(len(max_battery_value)):
    current_battery[i] -= 1
    if current_battery[i] == 0:
      current_battery[i] = max_battery_value[i]
      
  for i in range(len(max_water_value)):
    current_water[i] -= 1
    if current_water[i] == 0:
      current_water[i] = max_water_value[i]

  sleep(0.1)
