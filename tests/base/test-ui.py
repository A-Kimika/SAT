import sys
import time
import threading
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class plotArgs:
	win	=	None
	ax	=	None
	line	=	None
	canvas	=	None

class state:
	title	=	"default"
	y	=	None
	x	=	None
	ylimit	=	0
	xlimit	=	0

states = []
avgs = []

stateIndex = 0
currentState = state()

colour = "white"

device = '/dev/ttyACM0'

def setAvgState():
	global currentState
	global stateIndex
	global avgs
	
	currentState = avgs[stateIndex]

def avgPlot(pltState):
	s = 0
	if len(pltState.y) >= 10:
		for i in range(1, 11):
			s += pltState.y[len(pltState.y) - i]
	return s / 10

def cycleState():
	global stateIndex
	global currentState
	global states

	stateIndex += 1

	if stateIndex >= len(states):
		stateIndex = 0

	if len(states) != 0:
		currentState = states[stateIndex]

def plot(args):
	global currentState
	global colour

	n = currentState.x[len(currentState.x)-1]
	if n > currentState.xlimit:
		currentState.xlimit = n

	args.ax.set_title(currentState.title)
	y = currentState.y
	x = currentState.x
	ylim = currentState.ylimit
	xlim = currentState.xlimit

	args.ax.patch.set_facecolor(colour)
	
	args.ax.set_ylim(0, ylim)
	yval = range(0, ylim, 5)
	args.ax.set_yticks(yval)
	
	args.ax.set_xlim(0, xlim)
	xval = range(0, xlim, 10)
	args.ax.set_xticks(xval)

	args.line.set_data(x, y)

	args.canvas.draw_idle()

	args.win.after(16, lambda: plot(args))

def loop(win, start, stop):
	global receiverReady
	global satteliteReady
	global eps

	eps += 16

	if receiverReady == True and satteliteReady == True:
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

def window():
	print("main window starting...")

	global applicationRunning

	fig, ax = plt.subplots()
	line,   = ax.plot([], [])

	window = Tk()

	window.title('uwu')
	window.geometry("800x600")
	window.minsize(800, 600)

	window.rowconfigure(0, weight=2, minsize = 400)
	window.rowconfigure(1, weight=1, minsize = 40)
	window.rowconfigure(2, weight=1, minsize = 80)
	window.rowconfigure(3, weight=1, minsize = 80)

	window.columnconfigure(0, weight=1)
	window.columnconfigure(1, weight=1)
	window.columnconfigure(2, weight=1)
	
	cmd = Entry()
	cmd.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky=N + S + E + W)
	
	startButton = Button(window, text="START", bg='green', fg="white",command=lambda: send("START"))
	startButton.grid(row=2, column=0, padx=5, pady=5, sticky=N + S + E + W)

	stopButton = Button(window, text="STOP", bg='red', fg="white",command=lambda: send("STOP"))
	stopButton.grid(row=2, column=1, padx=5, pady=5, sticky=N + S + E + W)

	plotButon = Button(window, text="TEMPERATURE /\nHUMIDITY", bg='blue', fg="white",command=cycleState)
	plotButon.grid(row=2, column=2, padx=5, pady=5, sticky=N + S + E + W)
	
	A_Button = Button(window, text="SEND", bg='yellow', fg="black", command=lambda: send(cmd.get()))
	A_Button.grid(row=3, column=0, padx=5, pady=5, sticky=N + S + E + W)

	B_Button = Button(window, text="B", bg='grey', fg="white")  
	B_Button.grid(row=3, column=1, padx=5, pady=5, sticky=N + S + E + W)

	AVG_Buton = Button(window, text="Average", bg='blue', fg="white", command=setAvgState)
	AVG_Buton.grid(row=3, column=2, padx=5, pady=5, sticky=N + S + E + W)

	picture_frame = LabelFrame(window, text = 'plot')
	picture_frame.grid(row=0, column=0, columnspan=3, padx=0, pady=0, sticky=N + S + E + W)

	picture_frame.rowconfigure(0, weight=1)
	picture_frame.columnconfigure(0, weight=1)

	canvas = FigureCanvasTkAgg(fig, master=picture_frame)
	canvas.draw()

	canvas_widget = canvas.get_tk_widget()
	canvas_widget.grid(row=0, column=0, padx=0, pady=0, sticky=N + S + E + W)

	pArgs = plotArgs()

	pArgs.win = window
	pArgs.ax = ax
	pArgs.line = line
	pArgs.canvas = canvas

	loop(window, startButton, stopButton)
	plot(pArgs)

	window.mainloop()
	applicationRunning = False

eps = 1000

applicationRunning = True
receiverConnected = True
receiverReady = False
satteliteConnected = False
satteliteReady = False
satteliteError = False

threadRecepcion = threading.Thread (target = window)
threadRecepcion.start()

stateTMP = state()
stateTMP.title = "Temperature"
stateTMP.y = []
stateTMP.x = []
stateTMP.ylimit = 50
stateTMP.xlimit = 0

stateAVGTMP = state()
stateAVGTMP.title = "Average Temperature"
stateAVGTMP.y = []
stateAVGTMP.x = []
stateAVGTMP.ylimit = 50
stateAVGTMP.xlimit = 0

stateHUM = state()
stateHUM.title = "Humidity"
stateHUM.y = []
stateHUM.x = []
stateHUM.ylimit = 100
stateHUM.xlimit = 0

stateAVGHUM = state()
stateAVGHUM.title = "Average Humidity"
stateAVGHUM.y = []
stateAVGHUM.x = []
stateAVGHUM.ylimit = 100
stateAVGHUM.xlimit = 0

states.append(stateTMP)
states.append(stateHUM)

avgs.append(stateAVGTMP)
avgs.append(stateAVGHUM)

currentState = stateTMP

while applicationRunning and receiverConnected:
	i = len(stateTMP.x)
	j = len(stateHUM.x)
	
	stateTMP.x.append(i)
	stateHUM.x.append(j)
	
	stateTMP.y.append(math.sin(i/10) * 25 + 25)
	stateHUM.y.append(math.cos(j/10) * 50 + 50)
	
	if i%10 == 0:
		stateAVGTMP.x.append(len(stateAVGTMP.x)*10)
		stateAVGTMP.y.append(avgPlot(stateTMP))
		
	if j%10 == 0:
		stateAVGHUM.x.append(len(stateAVGHUM.x)*10)
		stateAVGHUM.y.append(avgPlot(stateHUM))
		
	time.sleep(0.1)