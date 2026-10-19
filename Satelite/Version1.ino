// Bibliotecas
#include <DHT.h>
#include <SoftwareSerial.h>
//Definiciones
#define DHTPIN 13
#define DHTTYPE DHT11
//Inicialización
DHT dht(DHTPIN, DHTTYPE);
const int led1 = 2;
SoftwareSerial Base(10, 11); // RX, TX (Rojo, Azul)

void setup() {
  //Literalmente el setup
  pinMode(led1, OUTPUT);
   digitalWrite(led1, LOW);
   Serial.begin(9600);
   Base.begin(9600);
   // Inicialización del sensor
   dht.begin();
}
void loop() {
  if (Base.available()) {

    //Detectar el mensaje
    String data = Base.readString();
    data.trim();
    Serial.println(data);

    //Empezar transmisión
      if (data == "START") {
        Base.println ("{R}"); //Envia confirmación de que ha recibido el mensaje (para que la estación siga enviando hasta que se confirme)

          while (data != "STOP"){
            /*
            if (data.length() > 0)
              data = data.toInt();
              Base.begin(data);
              SAT.println (cmd)
              Serial.println(cmd)
              Serial.begin(data)
              SAT.begin(data)*/
            delay(500);
            float h = dht.readHumidity();
            float t = dht.readTemperature();

            if (isnan(h) || isnan(t)) //Comprovación y aviso de error de detección

              Base.println("{ERROR}"); 

            else { //Enviamos todos los datos

              delay(500);
              digitalWrite(led1, HIGH);
              Base.print("{");
              Base.print(h);
              Base.print(";");
              Base.print(t);
              Base.println('}');
              digitalWrite(led1, LOW);}

            data = Base.readString();
            data.trim();
            if (data == "START")
              Base.println ("{R}");}

          Base.println ("{R}");}
   
   }
}