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
#define RGB_RED      12
#define RGB_GREEN    11

//water level pin array
const int WATER_PINS[5] = {WATER_20, WATER_40, WATER_60, WATER_80, WATER_100};
bool RGB_STATE[2] = {false, false};

const char* ssid = "HOME-WIFI";
const char* password = "87654321";
const char* mqtt_server = "broker.hivemq.com";
const char* device_id = "NF7";
const char* MQTT_DEVICE_ID = "NF7";
const char* MQTT_DEVICE_INTERVAL = "NF7-INTERVAL";
const char* MQTT_INTERVAL_TRIGGER = "NFFD-INTERVAL-TRIGGER";
const char* MQTT_DEVICE_NAME = "NF7-ESP8266";
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
unsigned long report_time = 0;
bool atomizer_on = false;

//millis parameter
const int ledPin1 =  LED_BUILTIN;// the number of the LED pin
int ledState1 = LOW;             // ledState used to set the LED
unsigned long previousMillis1 = 0;        // will store last time LED was updated
const long interval1 = 1000;           // interval at which to blink (milliseconds)

//previous values
int previous_water_level = 0;
int previous_battery = 0;
int previous_radar = 0;
bool first_run = true;

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

void setup() {
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
  pinMode(atomizer, OUTPUT);
pinMode(radar, OUTPUT);
  //init leds
  pinMode(RGB_BLUE, OUTPUT);
  pinMode(RGB_RED, OUTPUT);
  
  
  start_time = millis();

  Serial.println("MQTT init");
  Serial.print("Interval set to ");
  Serial.println(MQTT_DEVICE_INTERVAL);
  client.connect(MQTT_DEVICE_NAME);
  client.subscribe(MQTT_DEVICE_INTERVAL);
  client.loop();

  client.publish(MQTT_INTERVAL_TRIGGER, MQTT_DEVICE_ID);
  Serial.println("Awaiting interval...");
  start_time = millis();
  while (interval == 99) {
    client.publish(MQTT_INTERVAL_TRIGGER, MQTT_DEVICE_ID);
    Serial.print(".");
    delay(500);
    client.loop();
    //set to default value if no interval is set
    if (millis() - start_time > 10000) {
      interval = 10;
    }
  }
}

void loop() {
 if (!client.connected()) {
    reconnect();

  }

  client.loop();

  //every 3 second report the readings
  if (report_time + 1000 < millis()) {
    report_time = millis();
    int battery_level = read_battery();
    int WATER_level = read_water();
    int radar_value = read_radar();

    client.connect("ESP8266-B");

    //publish data to MQTT
    //{"NFFD-WATER", "NFFD-BATTERY", "NFFD-RADAR", "", ""};
    if (first_run) {
      send_data(0, WATER_level);
      send_data(1, battery_level);
      send_data(2, radar_value);
      first_run = false;
    } else {
      if (previous_water_level != WATER_level) {
        send_data(0, WATER_level);
        previous_water_level = WATER_level;
      }
      if (previous_battery != battery_level) {
        send_data(1, battery_level);
        previous_battery = battery_level;
      }
      if (previous_radar != radar_value) {
        send_data(2, radar_value);
        previous_radar = radar_value;
      }
    }
    
    Serial.print("BAT  : ");
    Serial.println(battery_level);
    Serial.print("WAT  : ");
    Serial.println(WATER_level);
    Serial.print("RAD  : ");
    Serial.println(radar_value);
    Serial.print("INT  : ");
    Serial.println(interval);
  }

  if (interval == 0) {
    if (!atomizer_on) {
      turn_on_atomizer();
    }
    atomizer_toggle = millis();
  }
  else if (interval == -1) {
    if (atomizer_on) {
      turn_off_atomizer();
    }
  }
  else {
    if (millis() > start_time + (interval * 1000)) {
      start_time = millis() + 2000;
      Serial.println(start_time);
      atomizer_toggle = millis();
      turn_on_atomizer();
    }
  }

  if (millis() > atomizer_toggle + 5000 && atomizer_on) {
    turn_off_atomizer();
  }

}

void send_data(int mqtt_topic_no, int data) {
  Serial.println("Sending " + String(MQTT_TOPICS[mqtt_topic_no]) + " with value " + String(data));
  static char convert_char[10];
  char* comma = ",";
  //add MQTT_DEVICE_ID to data
  dtostrf(data, 6, 2, convert_char);
  String data_string = MQTT_DEVICE_ID + String(comma) + String(convert_char);
  client.publish(MQTT_TOPICS[mqtt_topic_no], data_string.c_str());
}

void data(){
   int radar_value = read_radar();
   Serial.print("RAD  : ");
    Serial.println(radar_value);
  }

void turn_on_atomizer() {
  atomizer_on = true;
  Serial.println("Activating atomizer");
  digitalWrite(atomizer, HIGH);
}

void turn_off_atomizer() {
  atomizer_on = false;
  Serial.println("Deactivating atomizer");
  digitalWrite(atomizer, LOW);
}

void switch_rgb(int color) {
  //1 RED, 2 BLUE, 4 OFF

  digitalWrite(RGB_BLUE, LOW);
  digitalWrite(RGB_RED, LOW);

  if (color == 2) {
    digitalWrite(RGB_BLUE, HIGH);
    digitalWrite(RGB_RED, LOW);
  }
  else if (color == 1) {
    digitalWrite(RGB_BLUE, LOW);
    digitalWrite(RGB_RED, HIGH);
  }
  else if (color == 4) {
    digitalWrite(RGB_BLUE, LOW);
    digitalWrite(RGB_RED, LOW);
  }

}
