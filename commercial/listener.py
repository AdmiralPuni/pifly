import paho.mqtt.client as mqtt
from models.device import device
import time
import csv
import datetime

topic_list = ["NFFD-BATTERY", "NFFD-WATER", "NFFD-RADAR", "NFFD-INTERVAL-TRIGGER"]
db_field = ["battery", "water_level", "radar"]
latency_csv = 'csv/csvlatency.csv'

def insert_csv(device_id, start_time, received_time, delay_ms):
  timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
  with open(latency_csv, 'a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([timestamp, device_id, start_time, received_time, delay_ms])
  
def publish(client, topic, payload):
  client.publish(topic, payload, qos=0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  #print("Connected with result code "+str(rc))
  for topic in topic_list:
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  realmsg = str(msg.payload)[:-1]
  realmsg = realmsg[2:]
  topic = msg.topic
  if topic == "NFFD-INTERVAL-TRIGGER":
    interval = device.get_interval_by_serial_number(realmsg)
    publish(client, realmsg + "-INTERVAL", interval)
    return
  device_id, payload = realmsg.split(',')
  
  print("NEW MESSAGE FROM " + device_id + "==========================")
  print("RAW DATA   : " + realmsg)
  print("DATETIME   :", datetime.datetime.now())
  print("TOPIC      :", topic)
  print("DEVICE_ID  :", device_id)
  print("PAYLOAD    :", float(payload))
  #battery is bugged to 300%

  #align topic with database field
  if topic == "NFFD-BATTERY":
    topic = "battery"
  elif topic == "NFFD-WATER":
    topic = "water"
  elif topic == "NFFD-RADAR":
    topic = "radar"
  
  device.update_by_serial_number({'serial_number': device_id, topic: float(payload)})
  
  
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


print('PiFly listerner started')

client.connect("broker.hivemq.com", 1883, 60)
#clear the buffer
client.loop(2)


client.loop_forever()