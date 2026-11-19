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
      if(buf[i] == "ARM:1") {
          digitalWrite(13, HIGH);
      } else if(buf[i] == "ARM:0") {
          digitalWrite(13, LOW);
      } else {
        SAT.println(cmd);
      };
    };
  };


  if (SAT.available()) {
    digitalWrite(12, HIGH);
      String data = SAT.readString();  
      Serial.print(data);
    digitalWrite(12, LOW);
  };
};
