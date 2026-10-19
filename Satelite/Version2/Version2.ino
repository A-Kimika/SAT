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

//Variables

  //Booleans
    bool transmision = false;
    bool LimiteSuperado
    bool CalcularEnSatelite = false;
  //Int
    int i;
    int fase = 0;
    int medias = 0;
    
  //Unsigned longs
    unsigned long EsperaDisponible =  500;
    unsigned long VTransmision = 2000;
    unsigned long UltimoEnvio = 0;
    unsigned long UltimaEspera = 0;
    unsigned long EsperaLimiteSuperado = 0;

  //Floats
    float h;
    float t;
    float o = 0;
    float Tanteriores[10] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    float Tmedia = 0;
    float TmediasAnteriores[2] = [0, 0];
    float LimiteUsuario = 24;
  //Strings
    String comandos[10];
    String valores[10];

//Funciones
void start() 
{
  Base.println ("{R}");
  transmision = true;
}

void stop()
{
  Base.println ("{R}");
  transmision = false;
}

void RecibirMensaje()
{
  String data = Base.readString();
  data.trim();
  int principio = 0;
  i = 1;

  while (principio < data.length() && i<10) 
  { 
    //Comando
    int posicion = data.indexOf(';', principio);
    if (posicion == -1) break;
    
    comandos[i] = data.substring(principio, posicion);
    Serial.println(comandos[i]);

    //Valor
    principio = posicion + 1;
    posicion = data.indexOf(';', principio);
    if (posicion == -1){
    valores[i] = data.substring(principio);
    Serial.println(valores[i]);
    principio = data.length();
    }
    else {
      valores[i] = data.substring(principio, posicion);
      principio = posicion + 1;
      
    }
    i++;
  }
}

void InterpretarComandos()
{
  for (int j = 1; j < i; j++)
  
  if (comandos[j] == "SS")
  {
    StartStop(valores[j]);
  }
  
  else if (comandos[j] == "V")
  {
    CambiarVTr(valores[j]);
  }
  
  else if (comandos[j] == "O")
  {
    CambiarOrientacion(valores[j]);
  }

  else if (comandos[j] == "CTM")

  /*else if (comandos[1] == "B")
  {
    Base.begin(valores[1].toInt());
    Serial.begin(valores[1].toInt());
  }*/

}

void StartStop(String valor)
{
  if (valor == "1")
    start();
  else if (valor == "0")
    stop();
}

void CambiarVTr(String valor)
{
  if (valor.toInt() > 1)
    VTransmision = valor.toInt()*1000UL;
}

void CambiarOrientacion(String valor)
{
  if ((valor == "0") || (valor.toFloat()) <= 359 && valor.toFloat() >= 0.1)
    o = valor.toFloat();
}

void LeerSensorDHT()
{
  h = dht.readHumidity();
  t = dht.readTemperature();
  Tanteriores[fase] = t;
  fase++;
}

void CalcularTemperaturaMedia()
{
  if (CalcularEnSatelite)
  {
    if (media == 2)
      media = 0

    if (fase == 10)
      fase = 0
    
    Tmedia = 0;
    
    for (j = 0; j < 10; j++)
    {
      Tmedia = Tmedia + Tanteriores[j];
    }
    
    Tmedia = Tmedia/10;
    TmediasAnteriores[media] = Tmedia;
    media++;
    k = 0;
    bool encontrado = false;
    if (Tmedia > LimiteUsuario)
    {
      while (!encontrado && k < 2)
      {
        if (TmediasAnteriores[k] < LimiteUsuario)
          encontrado = true;
      }
    }
    else
    {
      encontrado = true;
      LimiteSuperado = False;
    }
    if (!encontrado)
      LimiteSuperado = True;
  }
  else
  {
    TmediasAnteriores[0] = 0;
    TmediasAnteriores[1] = 0;

    for (j = 0; j < 10; j++)
      Tanteriores[j] = 0;
  }
}

void EnviarDHT()
{
  digitalWrite(led1, HIGH);
  Base.print("{H:");
  Base.print(h);
  Base.print(";T:");
  Base.print(t);
  Base.println('}');
  digitalWrite(led1, LOW);
  UltimoEnvio = millis();
}

void Disponible()
{
  Base.println("{T}");
  UltimaEspera = millis();
}

void RecibiendoTransmision()
{ 
  Base.println("{T}");
}

void ErrorLimiteSuperado()
{
  Base.println ("{ERROR}")
  EsperaLimiteSuperado = millis();
}

void ErrorDeteccion()
{
  Base.println("{ERROR}"); 
  UltimoEnvio = millis();
}

void setup() 
{
  //Literalmente el setup
  pinMode(led1, OUTPUT);
  digitalWrite(led1, LOW);
  Serial.begin(9600);
  Base.begin(9600);
  // Inicialización del sensor
  dht.begin();
}



void loop() 
{
  if (millis() - UltimaEspera > EsperaDisponible)
  {
    Disponible();
  }

  if (millis() - EsperaLimiteSuperado > 500)
  {
    ErrorLimiteSuperado();
  }
  //Detectar el mensaje
  if (Base.available())
  {
    RecibirMensaje();
    InterpretarComandos();
  }

  //Transmisión
  if (transmision && millis() - UltimoEnvio >= VTransmision) 
  {  
    LeerSensorDHT();

    if (isnan(h) || isnan(t)) //Comprovación y aviso de error de detección

      ErrorDeteccion();

    else  //Enviamos todos los datos

      EnviarDHT();
  }
}
