// Bibliotecas
#include <DHT.h>
#include <SoftwareSerial.h>
#include <Servo.h>

//Definiciones
#define DHTPIN 13
#define DHTTYPE DHT11

//Inicialización
DHT dht(DHTPIN, DHTTYPE);
const int led1 = 2; 
Servo myServo;
SoftwareSerial Base(10, 11); // RX, TX (Rojo, Azul)

//Variables

  //Booleans
    bool transmision = false;
    bool LimiteSuperado = false;
    bool CalcularEnSatelite = false;
    bool Rotar = false;
  //Int
    int i;
    int j;
    int n = 0;
    int fase = 0;
    int medias = 0;
    int contador = 0;
    int TRIG = 7;
    int ECO = 6;
    int DuracionBarrida;
    int Distancia;
    int PINServo = 4;
    
  //Unsigned longs
    unsigned long EsperaDisponible =  1500;
    unsigned long VTransmision = 2000;
    unsigned long UltimoEnvio = 0;
    unsigned long UltimaEspera = 0;
    unsigned long EsperaLimiteSuperado = 0;
    unsigned long EsperaSensorDistancia = 1000;
    unsigned long EsperaRotar = 0; 

  //Floats
    float h;
    float t;
    float AnguloDeseado = 90;
    float o = 90;
    float Tanteriores[10] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
    float Tmedia = 0;
    float TmediasAnteriores[2] = {0, 0};
    float LimiteUsuario = 46.00;
  //Strings
    String comandos[10];
    String valores[10];

//Funciones
void start()  //Inicia la transmisión de datos
{
  Base.println ("{R}");
  transmision = true;
  Serial.println ("S1");
  EsperaSensorDistancia = millis();
}

void stop() //Detiene la transmisión de datos
{
  Base.println ("{R}");
  transmision = false;
  Serial.println("S2");
}

void RecibirMensaje() //Lee los mensajes de la base
{ 
  Serial.println ("Recibo");
  String data = Base.readString();
  data.trim(); 
  Serial.println(data);
  int principio = 0;
  i = 1; 

  while (principio < data.length() && i<10) 
  { 
    //Comando
    int posicion = data.indexOf(':', principio); 
    if (posicion == -1) break;
    
    comandos[i] = data.substring(principio, posicion);
    Serial.println(comandos[i]);

    //Valor 
    principio = posicion + 1;
    posicion = data.indexOf(':', principio);
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

void InterpretarComandos() //Utiliza los mensajes de la base para llevar a cabo los comandos
{
  //for (int j = 1; j < i; j++)
  
  if (comandos[1] == "SS") //Transmision
  {
    StartStop(valores[1]);
  }
  
  else if (comandos[1] == "V") //Velocidad de intercambio de datos
  {
    CambiarVTr(valores[1]);
  }
  
  else if (comandos[1] == "O") //Orientación sensor de distancia
  {
    IniciarRotacion(valores[1]);
  }

  else if (comandos[1] == "CTM") //Calcular en satélite
  {
    Base.println("{R}");  
    if (valores[1] == '1')
      CalcularEnSatelite = true;
    else if (valores[1] == '0')
      CalcularEnSatelite = false;
    else
      Base.println ("Valor inválido");
  }

  else 
    Base.println ("{ERROR}");
    Base.println("{R}");
  /*else if (comandos[1] == "B")
  {
    Base.begin(valores[1].toInt());
    Serial.begin(valores[1].toInt());
  }*/

}

void StartStop(String valor) //Se encarga de, según el valor del comando, llamar a start o stop
{
  if (valor == "1")
    start();
  else if (valor == "0")
    stop();
}

void CambiarVTr(String valor) //Cambia la velocidad de intercambio de datos
{
  if (valor.toInt() >= 1)
    VTransmision = valor.toFloat()*1000UL;
    Serial.println(VTransmision); 
    Base.println("{R}");
}

//Funciones del Servo
void IniciarRotacion(String valor)
{
  float nuevoAngulo = valor.toFloat();
  if ((valor == "0") || (nuevoAngulo <= 180 && nuevoAngulo > 0))
  {
    AnguloDeseado = nuevoAngulo;
    Rotar = true;
  }
}

void CambiarOrientacion()
{
  if (millis() - EsperaRotar >= 15) // Velocidad: 15ms por paso
  {
    EsperaRotar = millis();
    float diferencia = AnguloDeseado - o;

    if (abs(diferencia) <= 1.0)
    {
      o = AnguloDeseado;
      myServo.write((int)o);
      Rotar = false;
    }
    else if (diferencia > 0)
    {
      o = o + 1.0;
      myServo.write((int)o);
    }
    else
    {
      o = o - 1.0;
      myServo.write((int)o);
    }
  }
}

void LeerSensorDHT() //Lee la información del sensor de humedad y temperatura
{
  h = dht.readHumidity();

  t = dht.readTemperature();
   if (!isnan(t))
  {
    Tanteriores[fase] = t;
    fase = (fase + 1) % 10;
  }
}

void CalcularTemperaturaMedia() //Calcula la temperatura media 
{
  Serial.print("CalcularEnSatelite: ");
  Serial.println(CalcularEnSatelite);

  if (medias == 2)
    medias = 0;

  Tmedia = 0;
  
  for (j = 0; j < 10; j++)
  {
    Tmedia = Tmedia + Tanteriores[j];
  }
  
  if (n < 10)
    n = n+1;
  Tmedia = Tmedia/n;
  Serial.println(Tmedia);
  Base.print ("{MT:");
  Base.print (Tmedia);
  Base.println("}");

  if (Tmedia > LimiteUsuario)
    contador++;
  else
    contador = 0;
  if (contador >= 3)
    LimiteSuperado = true;
  else
    LimiteSuperado = false;
} 

void EnviarDHT() //Función lógica que envia los datos
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

void Disponible() //Heartbeat
{
  Base.println("{T}");
  UltimaEspera = millis();
}

void ErrorLimiteSuperado() //En caso de que las 3 últimas temperaturas medias superen el máximo, se activa
{
  Base.println ("{ERROR}");
  EsperaLimiteSuperado = millis();
}

void ErrorDeteccion() //Si la infomación del sensor DHT es incorrecta o no hay envia error
{
  Base.println("{ERROR}"); 
  UltimoEnvio = millis();
}

void setup() 
{
  //Literalmente el setup
  myServo.attach(PINServo);
  pinMode (TRIG, OUTPUT);
  pinMode (ECO, INPUT);
  pinMode(led1, OUTPUT);
  digitalWrite(led1, LOW);
  Serial.begin(9600);
  Base.begin(9600);
  Base.setTimeout(50);
  // Inicialización del sensor
  dht.begin();
  myServo.write(90);
}

void CalcularDistancia () //Función que calcula la distancia entre un objeto y el sensor
{
  digitalWrite (TRIG, HIGH);
  if (millis() - EsperaSensorDistancia > 1000)
    digitalWrite (TRIG, LOW);
    DuracionBarrida = pulseIn(ECO, HIGH);
    Distancia = DuracionBarrida/58.2;
    Base.print ("{D:");
    Base.print (Distancia);
    Base.println ("}");
    EsperaSensorDistancia = millis();  
    if ((Distancia <= D_men) && (Distancia > 0))
      D_men = Distancia;
}

void loop() 
{  

  if (Rotar == true)
  {
    CambiarOrientacion();
  }

  if (millis() - UltimaEspera >= EsperaDisponible)
  {
    Disponible();
  }

  if ((millis() - EsperaLimiteSuperado > 1500) && (LimiteSuperado == true))
  {
    ErrorLimiteSuperado();
  }
  //Detectar el mensaje
  
  if (Base.available())
  {
    Serial.println ("Base funciona");
    RecibirMensaje();
    InterpretarComandos();
  }
  //Transmisión
  if ((transmision) && (millis() - UltimoEnvio >= VTransmision))
  { 
    LeerSensorDHT();
    CalcularDistancia();

    if (CalcularEnSatelite == true)
      CalcularTemperaturaMedia();

    if (isnan(h) || isnan(t)) //Comprovación y aviso de error de detección

      ErrorDeteccion();

    else  //Enviamos todos los datos

      EnviarDHT();
  }
}