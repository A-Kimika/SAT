#include <SoftwareSerial.h>

float i = 0;

int t1 = 0;
int t2 = 0;

int timer = 0;

bool sendAvg = false;

void setup() {
  Serial.begin(9600);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  t1 = millis();
  t2 = millis();
}

void loop() {
  i += 0.1;

  int dt = t2 - t1;
  timer += dt;
  t1 = millis();

  Serial.println("{RDY}");
  Serial.println("{T}");

  String cmd = Serial.readString();
  
  String buf[10];
  int index = 0;
  int count = 0;

  if(cmd != "") {
    while(index < cmd.length() - 1) {
        int newIndex = cmd.indexOf(';', index);
        buf[count] = cmd.substring(index, newIndex);
        index = newIndex + 1;
        count++;
    };

    for(int i = 0; i < count; i++) {
      if(buf[i] == "CMT:1")
        sendAvg = true;    
        
      if(buf[i] == "CMT:0")
        sendAvg = false;
    };
  };
  if (timer > 1000) {
    timer = 0;

    Serial.print("{");
      Serial.print("H:");
        Serial.print(sin(i) * 50 + 50);
    Serial.print(";");
      Serial.print("T:");
      Serial.print(cos(i) * 25 + 25);
    Serial.println('}');

    if(sendAvg) {
      Serial.print("{");
        Serial.print("MT:");
          Serial.print(25);
      Serial.print(";");
        Serial.print("MH:");
        Serial.print(50);
      Serial.println('}');
    };
  };

  if(cmd != "")
    Serial.println("{R}");
  t2 = millis();
}
