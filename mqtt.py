import paho.mqtt.client as mqtt
import json
import mysql.connector
from tqdm import tqdm

database = mysql.connector.connect(
    host='localhost',
    user='pi',
    password='',
    database='dbmqtt'
)

database_cursor = database.cursor()

json_file = 'database.json'
json_data = {
    'notification' : 23
}

progress_battery = tqdm(total = 100)
progress_battery.desc = "Battery-1"
progress_battery.refresh()

devices = []
devices.append([])
topics = ['battery', 'water_level']

devices[0].append('notification')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    for top in topics:
        client.subscribe(top)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    realmsg = str(msg.payload)[:-1]
    realmsg = realmsg[2:]
    #print(msg.topic, realmsg)
    
    for top in topics:
        if top == msg.topic:
            if top == 'battery':
                progress_battery.n = (float(realmsg))
                progress_battery.refresh()
            sql = 'UPDATE devices SET ' + top + '=' + str(float(realmsg))
            database_cursor.execute(sql)
            database.commit()
            json_data[top] = str(realmsg)
            with open(json_file, 'w') as f:
                json.dump(json_data, f)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.15", 1883, 60)

client.loop_forever()
