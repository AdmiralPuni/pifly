//import mqtt library
#include <PubSubClient.h>
#include <WiFi.h>

#define battery D0
#define water_20 D1
#define water_40 D2
#define water_60 D3
#define water_80 D4
#define water_100 D5
#define radar D6
#define atomizer D7
#define analog A0

const char* ssid = "Toko Bangunan";
const char* password = "ponorogo";
const char* mqtt_server = "192.168.0.15";
const char* device_id = "NFX";

WiFiClient espClient;
PubSubClient client(espClient);

int analogInPin  = A0;    // Analog input pin
int sensorValue;          // Analog Output of Sensor
float calibration = 0;
int bat_percentage;
int interval = 99;
unsigned long start_time = 0;
unsigned long atomizer_toggle = 0;
bool atomizer_on = false;

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected - ESP IP address: ");
  Serial.println(WiFi.localIP());
}

void setup(){
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  byte willQoS = 0;
  const char* willTopic = "willTopic";
  const char* willMessage = "My Will Message";
  boolean willRetain = false;
  client.connect("ESP8266-X", willTopic, willQoS, willRetain, willMessage);

  static char convert_char[7];
  
  for(int i = 1;i<=1000;i++){
    dtostrf(i, 6, 2, convert_char);
    client.publish("NFX-QOS", convert_char);
    //delay(10);
    Serial.println(i);
  }
}

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
  Serial.println();
  interval = converted.toInt();
}

// This functions reconnects your ESP8266 to your MQTT broker
// Change the function below if you want to subscribe to more topics with your ESP8266 
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");  
      // Subscribe or resubscribe to a topic
      // You can subscribe to more topics (to control more LEDs in this example)
      client.subscribe(device_id);
      client.subscribe("ping");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {
  
}
