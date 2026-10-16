#include <SoftwareSerial.h>
SoftwareSerial SAT(10, 11); //RX TX

void setup() {
  Serial.begin(9600);
  SAT.begin(9600);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
  pinMode(8, OUTPUT);
}

int eps = 0;
int t1 = 0;
int t2 = 0;

void alarm() {
  t2 = millis();
  if(t2 - t1 >= (1000/440))
  {
    t1 = millis();
    digitalWrite(8, HIGH);
  } else {
    digitalWrite(8, LOW);
  }
  
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
        alarm();
      } else {
        digitalWrite(13, LOW);
      }
        
    digitalWrite(12, LOW);
  }
  
  if(cmd != "") 
    SAT.println(cmd);
}
