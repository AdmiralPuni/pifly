//import mqtt library
#include <PubSubClient.h>
#include <ESP8266WiFi.h>

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
const char* device_id = "NF1";

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
  pinMode(battery, OUTPUT);
  pinMode(water_20, OUTPUT);
  pinMode(water_40, OUTPUT);
  pinMode(water_60, OUTPUT);
  pinMode(water_80, OUTPUT);
  pinMode(water_100, OUTPUT);
  pinMode(radar, OUTPUT);
  pinMode(atomizer, OUTPUT);
  start_time = millis();

  client.connect("ESP8266-B");
  client.subscribe(device_id);
  client.subscribe("ping");
  client.loop();
  static char convert_char[7];
  int start_code = 111;
  dtostrf(start_code, 6, 2, convert_char);
  
  client.publish("NF1-start", convert_char);
  Serial.println("Awaiting interval...");
  start_time = millis();
  while(interval == 99){
    client.publish("NF1-start", convert_char);
    Serial.print(".");
    delay(500);
    client.loop();
    if(start_time + 5000 > millis()){
      interval = 15;
    }
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
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  int battery_level = read_battery();
  int water_level = read_water();
  int radar_value = read_radar();
  
  client.connect("ESP8266-B");
  static char convert_char[7];
  dtostrf(water_level, 6, 2, convert_char);
  client.publish("NF1-water_level", convert_char);
  dtostrf(battery_level, 6, 2, convert_char);
  client.publish("NF1-battery", convert_char);
  dtostrf(radar_value, 6, 2, convert_char);
  client.publish("NF1-radar", convert_char);
  Serial.print("BAT  : ");
  Serial.println(battery_level);
  Serial.print("WAT  : ");
  Serial.println(water_level);
  Serial.print("RAD  : ");
  Serial.println(radar_value);
  Serial.print("INT  : ");
  Serial.println(interval);

  if(interval == 0){
    if(!atomizer_on){
      turn_on_atomizer();
    }
    atomizer_toggle = millis();
  }
  else if(interval == -1){
    if(atomizer_on){
      turn_off_atomizer();
    }
  }
  else{
    if(millis() > start_time + (interval * 1000)){
      start_time = millis() + 2000;
      Serial.println(start_time);
      atomizer_toggle = millis();
      turn_on_atomizer();
    }
  }

  if(millis() > atomizer_toggle + 5000 && atomizer_on){
    turn_off_atomizer();
  }
}

int read_analog(){
  return analogRead(analog);
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max){
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

int read_radar(){
  digitalWrite(radar, HIGH);
  delay(1500);
  int value = analogRead(analog);
  digitalWrite(radar, LOW);
  delay(50);

  return value;
}

int read_battery(){
  int level = 0;
  digitalWrite(battery, HIGH);
  delay(50);
  level = analogRead(analog);
  digitalWrite(battery, LOW);
  delay(50);

  float voltage = (((level * 3.3) / 1024) * 2 + 0); //multiply by two as voltage divider network is 100K & 100K Resistor
 
  int bat_percentage = mapfloat(voltage, 2.8, 4.2, 0, 100); //2.8V as Battery Cut off Voltage & 4.2V as Maximum Voltage
  bat_percentage = ((voltage)/(4.2))*100;

  return bat_percentage*2;
}

int read_water(){
  int level = 0;
  digitalWrite(water_20, HIGH);
  delay(50);
  if(read_analog() > 200){
    level = 20;
  }
  digitalWrite(water_20, LOW);
  delay(50);
  
  digitalWrite(water_40, HIGH);
  delay(50);
  if(read_analog() > 200){
    level = 40;
  }
  digitalWrite(water_40, LOW);
  delay(50);
  
  digitalWrite(water_60, HIGH);
  delay(50);
  if(read_analog() > 200){
    level = 60;
  }
  digitalWrite(water_60, LOW);
  delay(50);
  
  digitalWrite(water_80, HIGH);
  delay(50);
  if(read_analog() > 200){
    level = 80;
  }
  digitalWrite(water_80, LOW);
  delay(50);
  
  digitalWrite(water_100, HIGH);
  delay(50);
  if(read_analog() > 200){
    level = 100;
  }
  digitalWrite(water_100, LOW);
  delay(50);

  return level;
}

void turn_on_atomizer(){
  atomizer_on = true;
  Serial.println("Activating atomizer");
  digitalWrite(atomizer, LOW);
  delay(100);
  digitalWrite(atomizer, HIGH);
  delay(100);
  digitalWrite(atomizer, LOW);
}

void turn_off_atomizer(){
  atomizer_on = false;
  Serial.println("Deactivating atomizer");
  digitalWrite(atomizer, LOW);
  delay(100);
  digitalWrite(atomizer, HIGH);
  delay(100);
  digitalWrite(atomizer, LOW);
  delay(100);
  digitalWrite(atomizer, LOW);
  delay(100);
  digitalWrite(atomizer, HIGH);
  delay(100);
  digitalWrite(atomizer, LOW);
}
