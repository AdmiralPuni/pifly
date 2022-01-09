import paho.mqtt.client as mqtt
from tqdm import tqdm
import sql

topic_list = ['battery', 'water_level', 'radar', 'start']

def publish(client, topic, payload):
  client.publish(topic, payload, qos=0)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  #print("Connected with result code "+str(rc))
  client.subscribe('#')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  realmsg = str(msg.payload)[:-1]
  realmsg = realmsg[2:]
  #print(msg.topic, realmsg)
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

client.connect("34.127.121.177", 1883, 60)

client.loop_forever()
