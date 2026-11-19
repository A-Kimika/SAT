import sys
import serial
import time
import threading
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# window and plot data

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

# initial variables

states = []

tmpAlarm = 100

pt = time.monotonic()

stateIndex = 0
currentState = state()

avgCalculation = "local"

colour = "white"

device = '/dev/ttyACM0'

# switch for the average calculation handling
# accepts the button to update the text with the current status

def setAvgState(btn):
	global avgCalculation
	
	if avgCalculation == "local":
		avgCalculation = "remote"
		send("CMT:1",True)
		btn.configure(text = "AVERAGE (remote)", bg='orange')

	elif avgCalculation == "remote":
		avgCalculation = "local"	
		send("CMT:0",True)
		btn.configure(text = "AVERAGE   (local)", bg='blue')

# average of the last 10 values

def avgPlot(pltState):
	s = 0
	if len(pltState.y) >= 10:
		for i in range(1, 11):
			s += pltState.y[len(pltState.y) - i]
	return s / 10

# switch for the currently shown plot

def cycleState():
	global stateIndex
	global currentState
	global states

	stateIndex += 1

	if stateIndex >= len(states):
		stateIndex = 0

	if len(states) != 0:
		currentState = states[stateIndex]

# draw the currently shown plot, accepts window data structure

def plot(args):
	global currentState
	global colour

	args.ax.patch.set_facecolor(colour)
	
	if (len(currentState.x) >= 1) and (len(currentState.y) >= 1):
		n = currentState.x[len(currentState.x)-1]
		if n > currentState.xlimit:
			currentState.xlimit = n

		args.ax.set_title(currentState.title)
		y = currentState.y
		x = currentState.x
		ylim = currentState.ylimit
		xlim = currentState.xlimit
		
		args.ax.set_ylim(0, ylim)
		yval = range(0, ylim, 5)
		args.ax.set_yticks(yval)
		
		args.ax.set_xlim(0, xlim)
		xval = range(0, xlim, 10)
		args.ax.set_xticks(xval)

		args.line.set_data(x, y)

		args.canvas.draw_idle()
	args.win.after(16, lambda: plot(args))

# main window loop

def loop(win, start, stop, send):
	global receiverReady
	global satteliteWaiting
	global responseTimer
	global alarmTimer
	global pt

	dt = (time.monotonic() - pt)
	responseTimer += dt
	alarmTimer += dt
	pt = time.monotonic()

	if receiverReady and not satteliteWaiting:
		start.configure(state=NORMAL)
		stop.configure(state=NORMAL)
		send.configure(state=NORMAL)
	else:
		start.configure(state=DISABLED)
		stop.configure(state=DISABLED)
		send.configure(state=DISABLED)

	win.after(16, lambda: loop(win, start, stop, send))

# handle command line input

def command(cmd):
	global tmpAlarm
	if cmd.startswith("setPeriod:"):
		send("V:" + cmd.strip("setPeriod:"), True)

	if cmd.startswith("setAlarm.T:"):
		tmpAlarm = float(cmd.strip("setAlarm.T:"))

# send a message over serial, terminating ';' is added at the end
# accepts the message string and the wait flag

def send(msg, wait):
	global satteliteWaiting
	msg = msg + ";"

	if wait:
		satteliteWaiting = wait
	print("(OUT):", msg)
	mySerial.write(msg.encode('utf-8'))

# window initialisation

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
	window.columnconfigure(3, weight=1)

	cmd = Entry()
	cmd.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=N + S + E + W)
		
	infoLabel = Label(window, text = "Commands:\nsetPeriod:'n' (secs)\nsetAlarm.T:'n' (C°)", font=("Courier", 8))
	infoLabel.grid(row=0, column=3, rowspan=4, padx=5, pady=5, sticky=N)

	startButton = Button(window, text="START", bg='green', fg="white",command=lambda: send("SS:1", True))
	startButton.grid(row=2, column=0, padx=5, pady=5, sticky=N + S + E + W)

	stopButton = Button(window, text="STOP", bg='red', fg="white",command=lambda: send("SS:0", True))
	stopButton.grid(row=2, column=1, padx=5, pady=5, sticky=N + S + E + W)

	plotButon = Button(window, text="NEXT PLOT", bg='purple', fg="white",command=cycleState)
	plotButon.grid(row=2, column=2, padx=5, pady=5, sticky=N + S + E + W)
	
	sendButton = Button(window, text="EXEC", bg='yellow', fg="black", command=lambda: command(cmd.get()))
	sendButton.grid(row=1, column=2, padx=5, pady=5, sticky=N + S + E + W)

	A_Button = Button(window, text="A", bg='grey', fg="white")  
	A_Button.grid(row=3, column=0, padx=5, pady=5, sticky=N + S + E + W)

	B_Button = Button(window, text="B", bg='grey', fg="white")  
	B_Button.grid(row=3, column=1, padx=5, pady=5, sticky=N + S + E + W)

	AVG_Button = Button(window, text="AVERAGE  (local)", bg='blue', fg="white", command=lambda: setAvgState(AVG_Button))
	AVG_Button.grid(row=3, column=2, padx=5, pady=5, sticky=N + S + E + W)

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

	loop(window, startButton, stopButton, sendButton)
	plot(pArgs)

	window.mainloop()
	applicationRunning = False

# runtime variables

responseTimer = 0
alarmTimer = 0

applicationRunning = True
receiverConnected = False
receiverReady = False
satteliteConnected = False
satteliteWaiting = False
satteliteError = False
alarmOn = False

# receiver connection

try:
	mySerial = serial.Serial(device, 9600)
	receiverConnected = True
	print(mySerial)
except:
	print(f"could not open '{device}'")
	receiverConnected = False

threadRecepcion = threading.Thread (target = window)
threadRecepcion.start()

# plot data initialisation

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

stateDistance = state()
stateDistance.title = "Distance"
stateDistance.y = []
stateDistance.x = []
stateDistance.ylimit = 100
stateDistance.xlimit = 0

stateAVGDistance = state()
stateAVGDistance.title = "Average Distance"
stateAVGDistance.y = []
stateAVGDistance.x = []
stateAVGDistance.ylimit = 100
stateAVGDistance.xlimit = 0

states.append(stateTMP)
states.append(stateHUM)
states.append(stateDistance)

states.append(stateAVGTMP)
states.append(stateAVGHUM)
states.append(stateAVGDistance)

currentState = stateTMP

# main communication loop

while applicationRunning and receiverConnected:
	if responseTimer >= 5:
		send("ARM:1", False)
		print("Sattelite response timeout")
		satteliteConnected = False
		satteliteWaiting = False
		responseTimer = 0

	if mySerial.in_waiting > 0:
		try:
			line = mySerial.readline().decode('utf-8').rstrip()
			print(" (IN):", line)
			if line.startswith('{') and line.endswith('}'):
				line = line.strip("{}")
				match line:
					case "RDY":
						receiverReady = True
					case "T":
						responseTimer = 0
						satteliteConnected = True
					case "R":
						satteliteWaiting = False
					case "ERROR":
						satteliteError = True
					case _:
						satteliteError = False
						data = line.split(';')
						for entry in data:
							match entry[0]:
								case "M":
									match entry[1]:
										case "T":
											AT = float(entry.strip("MT:"))
											stateAVGTMP.x.append(len(stateAVGTMP.x))
											stateAVGTMP.y.append(AT)
										case "H":
											AH = float(entry.strip("MH:"))
											stateAVGHUM.x.append(len(stateAVGHUM.x))
											stateAVGHUM.y.append(AH)
								case "T":
									i = len(stateTMP.x)
									T = float(entry.strip("T:"))
									stateTMP.x.append(i)
									stateTMP.y.append(T)
									if avgCalculation == "local":
										stateAVGTMP.x.append(len(stateAVGTMP.x))
										stateAVGTMP.y.append(avgPlot(stateTMP))

								case "H":
									j = len(stateHUM.x)
									H = float(entry.strip("H:"))
									stateHUM.x.append(j)
									stateHUM.y.append(H)
									if avgCalculation == "local":
										stateAVGHUM.x.append(len(stateAVGHUM.x))
										stateAVGHUM.y.append(avgPlot(stateHUM))
								case "D":
									j = len(stateDistance.x)
									D = float(entry.strip("D:"))
									stateDistance.x.append(j)
									stateDistance.y.append(D)
									if avgCalculation == "local":
										stateAVGDistance.x.append(len(stateAVGDistance.x))
										stateAVGDistance.y.append(avgPlot(stateDistance))
		except:
			print(f"could not decode input")

	if alarmTimer >= 1:
		ATlen = len(stateAVGTMP.y)
		if(ATlen > 3):
			c1 = stateAVGTMP.y[ATlen - 1] > tmpAlarm
			c2 = stateAVGTMP.y[ATlen - 2] > tmpAlarm
			c3 = stateAVGTMP.y[ATlen - 3] > tmpAlarm
			if(c1 and c2 and c3):
				alarmOn = True
			else:
				alarmOn = False
		alarmTimer = 0

		if(satteliteConnected and not satteliteError and not alarmOn):
			send("ARM:0", False)
			colour = "white"
		else:
			send("ARM:1", False)
			colour = "red"