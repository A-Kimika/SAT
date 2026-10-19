#include <SoftwareSerial.h>

float i = 0;

void setup() {
  Serial.begin(9600);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  i += 0.1;
  
  Serial.println("{RDY}");
  Serial.println("{T}");

  String cmd = Serial.readString();

  if(cmd == "{SS:0}" || cmd == "{SS:1}") 
    Serial.println("{R}");
  
  Serial.print("{");
    Serial.print("H:");
      Serial.print(sin(i) * 50 + 50);
  Serial.print(";");
    Serial.print("T:");
     Serial.print(cos(i) * 25 + 25);
  Serial.println('}');
}
