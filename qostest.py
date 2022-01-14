import paho.mqtt.client as mqtt
import time
import matplotlib.pyplot as plt

topic_list = ['NFX-QOS']
latencies = []
messages = []
latencies.append(time.time())

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
  #print("Connected with result code "+str(rc))
  client.subscribe('NFX-QOS', qos=0)
  #subscribe to NFX-QOS

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
  latencies.append(time.time())
  realmsg = str(msg.payload)[:-1]
  realmsg = realmsg[2:]
  messages.append(float(realmsg))
  print(realmsg)
  #if the message is 100 end the loop
  if realmsg == '1000.00':
    #print(latencies)
    client.disconnect()
    #check for missing messages
    loss = 0
    for i in range(0,1000):
      if i+1 not in messages:
        loss += 1
    print('Loss:', loss, '%')
    #calculate the average latency
    avg = 0
    for i in range(0, len(latencies)-1):
      avg += latencies[i+1] - latencies[i]
    avg = avg/(len(latencies)-1)
    print('Average latency:', avg*1000, 'ms')
    delays = []
    for i in range(1, len(latencies)-1):
      delays.append((latencies[i+1] - latencies[i])*1000)
    plt.plot(messages[:-1], delays)
    plt.ylabel('Latency (ms)')
    plt.show()
    return

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.0.15", 1883, 60)

client.loop_forever()
