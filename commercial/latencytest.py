import paho.mqtt.client as mqtt
import time
import csv
import datetime
import os

DEVICE_LIST = ['MONA', 'LISA', 'BOSSA', 'NOVA', 'TERRA', 'COTA']
TOPIC_NAME = 'NFFD-LATENCY-'
FILE_NAME = "1WAYLATENCY" + datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".csv"
FILE_PATH = "static/experiment/"

latency_csv = 'static/experiment/latency' + datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + '.csv'

#if file does not exist, create it
if not os.path.isfile(FILE_PATH + FILE_NAME):
  with open(FILE_PATH + FILE_NAME, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['serial_number', 'latency', 'timestamp'])

def log(data):
  #append data to csv file
  with open(FILE_PATH + FILE_NAME, 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

def publish(client, topic, payload):
  client.publish(topic, payload, qos=0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  #print("Connected with result code "+str(rc))
  for device in DEVICE_LIST:
    client.subscribe(TOPIC_NAME + device)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  realmsg = str(msg.payload)[:-1]
  realmsg = realmsg[2:]
  topic = msg.topic
  payload = realmsg.split(',')
  publish(client, "NFFD-LATENCY",  realmsg)

  #print
  print("=====================================")
  print("TOPIC      :", topic)
  print("RAW DATA   :", realmsg)
  #time diff
  time_diff = time.time() - float(realmsg.split(',')[-1])
  #convert unix time to ms
  time_diff = time_diff * 1000
  #round to 3 decimal places
  time_diff = round(time_diff, 3)


  

  print("LATENCY    :", time_diff)

  #log to csv
  log_data = []
  log_data.append([topic.split('-')[-1], time_diff, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
  log(log_data)

  #bounce back to device
  
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


print('PiFly listerner started')

client.connect("broker.hivemq.com", 1883, 60)
#clear the buffer
client.loop(2)


client.loop_forever()