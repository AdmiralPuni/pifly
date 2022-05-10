//import mqtt library
#include <PubSubClient.h>
#include <ESP8266WiFi.h>

#define battery      D0
#define WATER_20     D1
#define WATER_40     D2
#define WATER_60     D3
#define WATER_80     D4
#define WATER_100    D5
#define radar        D6
#define atomizer     D7
#define analog       A0

#define RGB_BLUE     D8
#define RGB_RED      D1
#define RGB_GREEN    D2

//water level pin array
const int WATER_PINS[5] = {WATER_20, WATER_40, WATER_60, WATER_80, WATER_100};
bool RGB_STATE[2] = {false, false};

const char* ssid = "Toko Bangunan";
const char* password = "ponorogo";
const char* mqtt_server = "broker.hivemq.com";
const char* device_id = "NF5";
const char* MQTT_DEVICE_ID = "NF5";
const char* MQTT_TOPICS[5] = {"NFFD-WATER", "NFFD-BATTERY", "NFFD-RADAR", "", ""};

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
  Serial.println("Connecting to MQTT broker");
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  Serial.println("Setting up pins");
  pinMode(battery, OUTPUT);
  pinMode(WATER_20, OUTPUT);
  pinMode(WATER_40, OUTPUT);
  pinMode(WATER_60, OUTPUT);
  pinMode(WATER_80, OUTPUT);
  pinMode(WATER_100, OUTPUT);
  pinMode(radar, OUTPUT);
  pinMode(atomizer, OUTPUT);

  //init leds
  pinMode(RGB_BLUE, OUTPUT);
  pinMode(RGB_RED, OUTPUT);

  start_time = millis();

  Serial.println("MQTT init");
  client.connect("NF2-ESP8266-B");
  client.subscribe(String(MQTT_DEVICE_ID + String("-INTERVAL")).c_str());
  client.loop();
  static char convert_char[7];
  int start_code = 111;
  dtostrf(start_code, 6, 2, convert_char);
  
  client.publish("NF2-start", convert_char);
  Serial.println("Awaiting interval...");
  start_time = millis();
  while(interval == 99){
    client.publish("NF2-start", convert_char);
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
  if(topic_converted == "NF2-INTERVAL"){
    interval = converted.toInt();
    Serial.print("Interval set to ");
    Serial.println(interval);
    return;
  }
  Serial.println();
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
  int WATER_level = read_water();
  int radar_value = read_radar();
  
  client.connect("ESP8266-B");

  //publish data to MQTT
  //{"NFFD-WATER", "NFFD-BATTERY", "NFFD-RADAR", "", ""};
  send_data(0, WATER_level);
  send_data(1, battery_level);
  send_data(2, radar_value);

  Serial.print("BAT  : ");
  Serial.println(battery_level);
  Serial.print("WAT  : ");
  Serial.println(WATER_level);
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

void send_data(int mqtt_topic_no, int data){
  Serial.println("Sending " + String(MQTT_TOPICS[mqtt_topic_no]) + " with value " + String(data));
  static char convert_char[10];
  char* comma = ",";
  //add MQTT_DEVICE_ID to data
  dtostrf(data, 6, 2, convert_char);
  String data_string = MQTT_DEVICE_ID + String(comma) + String(convert_char);
  client.publish(MQTT_TOPICS[mqtt_topic_no], data_string.c_str());
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

  if(bat_percentage < 30){
    switch_rgb(2);
  }

  return bat_percentage*2;
}

int read_water(){
  int water_treshold = 200;
  int level = 0;

  for(int i = 0; i < 5; i++){
    digitalWrite(WATER_PINS[i], HIGH);
    delay(50);
    if(read_analog() > water_treshold){
      level = (i+1) * 20;
    }
    digitalWrite(WATER_PINS[i], LOW);
    delay(50);
  }

  if(level == 20){
    switch_rgb(1);
  }

  return level;
}

void turn_on_atomizer(){
  atomizer_on = true;
  Serial.println("Activating atomizer");
  digitalWrite(atomizer, HIGH);
}

void turn_off_atomizer(){
  atomizer_on = false;
  Serial.println("Deactivating atomizer");
  digitalWrite(atomizer, LOW);
}

void switch_rgb(int color){
  //1 RED, 2 BLUE, 4 OFF

  digitalWrite(RGB_BLUE, LOW);
  digitalWrite(RGB_RED, LOW);

  if(color == 2){
    digitalWrite(RGB_BLUE, HIGH);
    digitalWrite(RGB_RED, LOW);
  }
  else if(color == 1){
    digitalWrite(RGB_BLUE, LOW);
    digitalWrite(RGB_RED, HIGH);
  }
  else if(color == 4){
    digitalWrite(RGB_BLUE, LOW);
    digitalWrite(RGB_RED, LOW);
  }

}
