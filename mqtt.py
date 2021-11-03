import paho.mqtt.client as mqtt
import json
import mysql.connector

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

devices = []
devices.append([])

devices[0].append('notification')

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("battery2")
    client.subscribe("battery")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    realmsg = str(msg.payload)[:-1]
    realmsg = realmsg[2:]
    print(msg.topic, realmsg)
    sql = 'UPDATE devices SET battery=' + str(float(realmsg))
    database_cursor.execute(sql)
    database.commit()
    if msg.topic == 'hello':
        json_data['notification'] = str(realmsg)
        with open(json_file, 'w') as f:
            json.dump(json_data, f)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.15", 1883, 60)

client.loop_forever()