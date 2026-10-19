import serial
import sys
import time
import threading
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class plotState:
	win		=	None
	ax		=	None
	line	=	None
	canvas	=	None

class state:
	title	=	"default"
	value	=	None
	limit	=	0

states = []

stateIndex = 0
currentState = state()

colour = "white"

device = '/dev/ttyACM0'

i = 0

xlim = 10
ylim = 50

x = []
y = []

xval = []
yval = []

def cycleState():
	global stateIndex
	global currentState
	global states

	stateIndex += 1

	if stateIndex >= len(states):
		stateIndex = 0

	if len(states) != 0:
		currentState = states[stateIndex]

def plot(pltState):
	global currentState

	global colour

	global i

	global xlim
	global ylim

	global x
	global y

	global xval
	global yval

	if(len(x) != 0):
		if x[len(x)-1] % 10 == 0:
			xval.append(x[len(x)-1])
		if x[len(x)-1] > xlim:
			pltState.ax.set_xlim(0, len(x)-1)

	pltState.ax.set_title(currentState.title)
	y = currentState.value

	ylim = currentState.limit

	pltState.ax.patch.set_facecolor(colour)
	pltState.ax.set_ylim(0, ylim)

	yval = range(0, ylim, 5)

	pltState.ax.set_xticks(xval)
	pltState.ax.set_yticks(yval)

	pltState.line.set_data(x, y)

	pltState.canvas.draw_idle()

	print("------------------")
	print(y)
	print(x)
	print(xlim)
	print(ylim)
	print(xval)
	print(yval)
	pltState.win.after(16, lambda: plot(pltState))

def loop(win, start, stop):
	global ready
	global wait
	global eps

	eps += 16

	if ready == True and wait == False:
		start.configure(state=NORMAL)
		stop.configure(state=NORMAL)
	else:
		start.configure(state=DISABLED)
		stop.configure(state=DISABLED)

	win.after(16, lambda: loop(win, start, stop))

def send(msg):
	global ready
	global wait

	print("(OUT):", msg)
	mySerial.write(msg.encode('utf-8'))
	ready = False
	wait = True

def window():
	print("main window starting...")

	global run

	fig, ax = plt.subplots()
	line,   = ax.plot([], [])

	window = Tk()

	window.title('uwu')
	window.geometry("800x600")
	window.minsize(800, 600)

	window.rowconfigure(0, weight=2, minsize = 400)
	window.rowconfigure(1, weight=1, minsize = 200)

	window.columnconfigure(0, weight=1)
	window.columnconfigure(1, weight=1)
	window.columnconfigure(2, weight=1)

	startButton = Button(window, text="START", bg='green', fg="white",command=lambda: send("START"))
	startButton.grid(row=1, column=0, padx=5, pady=5, sticky=N + S + E + W)

	stopButton = Button(window, text="STOP", bg='red', fg="white",command=lambda: send("STOP"))
	stopButton.grid(row=1, column=1, padx=5, pady=5, sticky=N + S + E + W)

	plotButon = Button(window, text="PLOT", bg='blue', fg="white",command=cycleState)
	plotButon.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)

	picture_frame = LabelFrame(window, text = 'plot')
	picture_frame.grid(row=0, column=0, columnspan=3, padx=0, pady=0, sticky=N + S + E + W)

	picture_frame.rowconfigure(0, weight=1)
	picture_frame.columnconfigure(0, weight=1)

	ax.set_xlim(0, xlim)
	ax.set_ylim(0, ylim)

	ax.set_xticks(xval)
	ax.set_yticks(yval)

	canvas = FigureCanvasTkAgg(fig, master=picture_frame)
	canvas.draw()

	canvas_widget = canvas.get_tk_widget()
	canvas_widget.grid(row=0, column=0, padx=0, pady=0, sticky=N + S + E + W)

	pState = plotState()

	pState.win = window
	pState.ax = ax
	pState.line = line
	pState.canvas = canvas

	loop(window, startButton, stopButton)
	plot(pState)

	window.mainloop()
	run = False

init = True

"""
try:
	mySerial = serial.Serial(device, 9600)
except:
	print(f"could not open '{device}'")
	init = False
"""

run = True
ready = False
wait = False
sync = False
error = False

threadRecepcion = threading.Thread (target = window)
threadRecepcion.start()

eps = 1000

stateTMP = state()
stateTMP.title = "Temperature"
stateTMP.value = []
stateTMP.limit = 50

stateHUM = state()
stateHUM.title = "Humidity"
stateHUM.value = []
stateHUM.limit = 100

states.append(stateTMP)
states.append(stateHUM)

currentState = stateTMP

while run and init:
	x.append(i)
	i += 1
	stateTMP.value.append(24)
	stateHUM.value.append(60)
	time.sleep(1)
"""
	if eps >= 1000:
		eps = 0
		sync = False
		wait = False
	
	if mySerial.in_waiting > 0:
		line = mySerial.readline().decode('utf-8').rstrip()
		print(" (IN):", line)
		if line.startswith('{') and line.endswith('}'):
			line = line.strip("{}")
			match line:
				case "RDY":
					ready = True
				case "T":
					sync = True
				case "R":
					wait = False
				case "ERROR":
					error = True
				case _:
					error = False
					data = line.split(';')
					for entry in data:
						match entry:
							case "T":
								T = float(entry.strip("T:"))
								stateTMP.value.append(T)
							case "H":
								H = float(entry.strip("H:"))
								stateHUM.value.append(H)
					x.append(i)
					i = i + 1

		if(sync == True and error == False):
				colour = "white"
		else:
				colour = "red"
"""