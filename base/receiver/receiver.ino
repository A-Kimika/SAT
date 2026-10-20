#include <SoftwareSerial.h>
SoftwareSerial SAT(10, 11); //RX TX

void setup() {
  Serial.begin(9600);
  SAT.begin(9600);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
}

void loop() {
  Serial.println("{RDY}");
  String cmd = Serial.readString();

  if (SAT.available()) {
    digitalWrite(12, HIGH);
      String data = SAT.readString();
      Serial.print(data);
      
      data.trim();
      if(data == "{ERROR}") {
        digitalWrite(13, HIGH);
        delay(100);
      } else {
        digitalWrite(13, LOW);
      }
        
    digitalWrite(12, LOW);
  }
  
  if(cmd != "") 
    SAT.println(cmd);
}
