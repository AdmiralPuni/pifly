#define ATOMIZER D7
#define TESTPIN D3

void setup(){
    pinMode(ATOMIZER, OUTPUT);
    pinMode(TESTPIN, OUTPUT);
}

void loop(){
    //activate both led builtin and atomizer
    digitalWrite(ATOMIZER, HIGH);
    digitalWrite(TESTPIN, HIGH);
    delay(1000);
    digitalWrite(ATOMIZER, LOW);
    digitalWrite(TESTPIN, LOW);
    delay(1000);
}