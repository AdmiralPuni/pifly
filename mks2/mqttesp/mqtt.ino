void callback(char* topic, byte* payload, unsigned int length) {
  String converted = "";
  String topic_converted = topic;
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i=0;i<length;i++) {
    Serial.print((char)payload[i]);
    converted += (char)payload[i];
  }
  if(topic_converted == "ping"){
    client.publish("ack-ping", device_id);
    Serial.println("Pinged");
    return;
  }
  if(topic_converted == MQTT_DEVICE_INTERVAL){
    interval = converted.toInt();
    Serial.print("Interval set to ");
    Serial.println(interval);
    return;
  }
  if(topic_converted == MQTT_TOPICS[3]){
    //reply with same topic and payload
    client.publish(MQTT_TOPICS[3], converted.c_str());
  }
  Serial.println();
}

// This functions reconnects your ESP8266 to your MQTT broker
// Change the function below if you want to subscribe to more topics with your ESP8266 
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(MQTT_DEVICE_NAME)) {
      Serial.println("connected");  
      // Subscribe or resubscribe to a topic
      // You can subscribe to more topics (to control more LEDs in this example)
      client.subscribe(MQTT_DEVICE_INTERVAL);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}