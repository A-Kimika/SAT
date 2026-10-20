# SAT Grupo 2
Somos el Grupo dos, compuesto por Aleksandr Kolesnikov y Sergi Fernández.

El proyecto se compone de una placa arduino conectada a un ordenador todo considerado el satlite y otra placa conectado a otro ordenador que en este caso es considerado base.

La carpeta Base contiene todos los scripts utilizados por la base y la placa arduino asociada a esta.
La carpeta Satelite contiene todo lo relacionado al satelite.

# DISTRIBUCIÓN

El satelite se encarga de contener los datos de sensores y mediante el lenguaje C en arduino se los envia por conexión a la otra placa, la base. La base se encarga de almacenar los datos e interpretarlos para hacer una gráfica, para ello, utiliza arduino para recibir la transmisión y recepción y una vez recolecta los datos, los envia a un código hecho con el lenguaje Python que hace toda la interpretación lógica de los datos.

# FUNCIONES

Las funciones disponibles para esta primera versión son las siguientes:
- Start: Empezar/Reanudar la transmisión de datos
- Stop: Detener la transmisión de datos
- Plot: Graficar los datos de humedad y temperatura detectados por el sensor DHT

# Interfaz

La interfaz contiene una grafica en la primera fila que se extiende hasta el final.
La segunda contiene una serie de 3 botones donde se encuentran el Start (verde con texto Start en blanco), Stop (rojo con texto Stop en blanco) y Temperature/Humidity (azul con texto en blanco, alterna la grafica que se observa).

Además, en caso de error, el fondo de la gráfica pasará a ser rojo y en el circuito un led rojo se encenderá. De la misma manera cuando todo funcione correctamente la gráfica permanecerá de color blanco y en el circuito se encenderá un led verde al recibir datos en el circuito de la base y un led verde se encenderá al enviar datos en el circuito del Satelite. 
