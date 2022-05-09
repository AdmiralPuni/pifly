import paho.mqtt.client as mqtt
from tqdm import tqdm
import sql
import time
import csv

topic_list = ['battery', 'water_level', 'radar', 'start', 'ack-ping']
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
  for identifier in sql.select_device_id():
    for topic in topic_list:
      client.subscribe(identifier + '-' + topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  realmsg = str(msg.payload)[:-1]
  realmsg = realmsg[2:]
  start_time = time.time()
  publish(client, 'ping', start_time)
  #print(msg.topic, realmsg)
  if msg.topic == 'ack-ping':
    current_time = time.time()
    received_time = round((current_time - start_time) * 1000,2)
    print('Received ack-ping from', realmsg)
    print(received_time, 'ms')
    print(current_time, start_time, current_time - start_time)
    insert_csv(realmsg, start_time, current_time, received_time)
    return
  for identifier in sql.select_device_id():
    for topic in topic_list:
      if msg.topic == identifier + '-' + topic:
        if topic == 'start':
          publish(client, identifier, sql.get_interval_single(identifier))
          print("Sending interval to " + identifier)
        else:
          sql.update_field(topic, realmsg, identifier)
          print('Updating device', identifier, 'with', topic, '=', realmsg)
  
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)
#clear the buffer
client.loop(2)


client.loop_forever()
