import paho.mqtt.client as mqtt
from models.device import device
import time
import csv
import datetime
import os

radar_trigger = {
  #'serial_number': {
  #  'prev_value': 0,
  #  'last_time': 0,
  #  'update_trigger': 0
  #}
}

FILE_NAME = "BBLATENCY" + datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + ".csv"
FILE_PATH = "static/experiment/"

radar_treshold = 200

TOPIC_LIST = ["NFFD-BATTERY", "NFFD-WATER", "NFFD-RADAR", "NFFD-INTERVAL-TRIGGER"]
db_field = ["battery", "water_level", "radar"]
latency_csv = 'static/experiment/latency' + datetime.datetime.now().strftime("%Y-%m-%dT%H-%M-%S") + '.csv'

DEVICE_LIST = ['MONA', 'LISA', 'BOSSA', 'NOVA', 'TERRA', 'COTA']
TOPIC_NAME = 'NFFD-LATENCY-'

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

def check_treshold(old, new):
  if old > radar_trigger and new > radar_trigger:
    return False
  elif old < radar_trigger and new < radar_trigger:
    return False
  else:
    return True
  
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
  for topic in TOPIC_LIST:
    client.subscribe(topic)
  #for device in DEVICE_LIST:
    #client.subscribe(TOPIC_NAME + device)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  skip_update = False
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

  #publish latency test
  publish(client, "NFFD-LATENCY-" + device_id, device_id + ',' + time.time())

  #align topic with database field
  if topic == "NFFD-BATTERY":
    topic = "battery"
  elif topic == "NFFD-WATER":
    topic = "water"
  elif topic == "NFFD-RADAR":
    topic = "radar"
  elif topic == "NFFD-LATENCY":
    log_data = []
    log_data.append([device_id, time.time() - float(payload), datetime.datetime.now()])
    log(log_data)

    #find serial in radar_delay
    #if device_id in radar_trigger:
    #  #check if update_trigger = 3
    #  if radar_trigger[device_id]['update_trigger'] == 3:
    #    skip_update = False
    #    radar_trigger[device_id]['update_trigger'] = 0
    #  else:
    #    if check_treshold(radar_trigger[device_id]['prev_value'], float(payload)):
    #      skip_update = True
    #    else:
    #      radar_trigger[device_id]['update_trigger'] += 1
    #      radar_trigger[device_id]['prev_value'] = float(payload)
    #  radar_trigger[device_id]['last_time'] = time.time()
    #else:
    #  radar_trigger[device_id] = {
    #    'prev_value': float(payload),
    #    'last_time': time.time(),
    #    'update_trigger': 0
    #  }

  if not skip_update:
    try:
      device.update_by_serial_number({'serial_number': device_id, topic: float(payload)})
    except:
      print("FAILED TO UPDATE DEVICE " + device_id + " WITH " + topic + ": " + payload)
  else:
    print("SKIPPING UPDATE FOR DEVICE " + device_id + " WITH " + topic + ": " + payload)
  
  
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message


print('PiFly listerner started')

client.connect("broker.hivemq.com", 1883, 60)
#clear the buffer
client.loop(2)


client.loop_forever()