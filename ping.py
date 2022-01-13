import paho.mqtt.client as mqtt
from tqdm import tqdm
import sql
import time

topic_list = ['ack-ping']

def publish(client, topic, payload):
  client.publish(topic, payload, qos=0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  #print("Connected with result code "+str(rc))
  client.subscribe('ack-ping')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  receive_time = time.time() - start_time
  realmsg = str(msg.payload)[:-1]
  realmsg = realmsg[2:]
  print(msg.topic, realmsg)
  #print the time in milliseconds
  print(receive_time * 1000)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("34.127.121.177", 1883, 60)

publish(client, 'ping', '0')
start_time = time.time()
#wait until on message

#print current time in unix format
print(time.time())

while True:
  print("Waiting for ping")
  start_time = time.time()
  publish(client, 'ping', time.time())

  time.sleep(2)


