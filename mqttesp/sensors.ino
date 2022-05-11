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