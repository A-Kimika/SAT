import serial
import sys
import time
import threading
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

TMP = False
HUM = True

colour = "white"

device = '/dev/ttyACM0'

tmp = []
hum = []

state = TMP

i = 0

xlim = 10
ylim = 50

x = []
y = []

xval = []
yval = []

def play():
	global state
	state = not state

def plot(win, ax, line, canvas):
	global i
	global colour

	global tmp
	global hum

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
			ax.set_xlim(0, len(x)-1)

	if state == TMP:
		ax.set_title('Temperature')
		y = tmp
		ylim = 45

	else:
		ax.set_title('Humidity')
		y = hum
		ylim = 100

	ax.patch.set_facecolor(colour)
	ax.set_ylim(0, ylim)
	yval = range(0, ylim, 5)
	ax.set_xticks(xval)
	ax.set_yticks(yval)

	line.set_data(x, y)

	canvas.draw_idle()


	win.after(100, lambda: plot(win, ax, line, canvas))

def send(msg):
	print("(OUT):", msg)

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

	plotButon = Button(window, text="PLOT", bg='blue', fg="white",command=play)
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

	plot(window, ax, line, canvas)

	window.mainloop()
	run = False

run = True

threadRecepcion = threading.Thread (target = window)
threadRecepcion.start()

while run:
		time.sleep(0.1)
		colour = "white"
		x.append(i)
		i = i + 1
		H = math.sin(i/10)*40 + 45
		T = math.cos(i/10)*20 + 25
		tmp.append(T)
		hum.append(H)