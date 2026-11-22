# SAT Grupo 2

### [Video V1](https://drive.google.com/file/d/1hvOzGaZAGr3G5iYpnstDdow7pwcVJ2ZW/view?usp=sharing)

### [Video V2](https://drive.google.com/file/d/1JZbxgElAuV3N5PwONAfIJCs6YoMQGQos/view?usp=sharing)

## INTRODUCCIÓN

El proyecto se compone de una placa arduino conectada a un ordenador todo considerado el satlite y otra placa conectado a otro ordenador que en este caso es considerado base.

La carpeta Base contiene todos los scripts utilizados por la base y la placa arduino asociada a esta.
La carpeta Satelite contiene todo lo relacionado al satelite.

## DISTRIBUCIÓN

El satelite se encarga de contener los datos de sensores y mediante el lenguaje C en arduino se los envia por conexión a la otra placa, la base. La base se encarga de almacenar los datos e interpretarlos para hacer una gráfica, para ello, utiliza arduino para recibir la transmisión y recepción y una vez recolecta los datos, los envia a un código hecho con el lenguaje Python que hace toda la interpretación lógica de los datos.

## FUNCIONES

Las funciones disponibles son las siguientes:
- Captura y transmisión de datos de temperatura, humedad y distancia
- Control de dirección del sensor de distancia
- Alarma de temperatura mayor que un valor determinado

## INTERFAZ

La interfaz contiene una lista de gráficas y una ventana con la lista de comandos disponibles.

## PROTOCOLO (Acción | Comando | Valores | Descripción)

- Empezar y Parar:	SS	| 1 o 0	| Si es 1 la transmisión continuará, si es 0 se detendrá	
- Cambiar velocidad de Transmisión:	V |	x (segundos)	| La diferencia de tiempo entre mensaje y mensaje variará	
- Cambiar orientación del satélite:	O	| 0-180º	| Cambiar la orientación del satelite	
- Cambiar frecuencia de Transmisión:	B	| x (baudios)	| Cambia la frecuencia en Baudios a la que se efectua la transmisión de datos	
- Calcular Temperatura Media:	CTM	| 1 o 0	| Si es un 1 el satelite se encargará de calcular la temperatura media, si es 0 no	

## USO

para abrir la programa que contiene el interfaz gráfico:

```
python ./base/ui.py
```

Es posible que sera necesario cambiar el port de comunicación:

```
device = '/dev/ttyACM0'
```

El port actual se puede ver en la implicación Arduino IDE

## TEST

Para comprobar el funcionamiento sin el segundo Arduino se puede usar la programa en /tests/base/sattelite-test para simular la conexión con un satélite
