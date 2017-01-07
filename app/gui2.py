import Tkinter
import tkMessageBox
import time
from PIL import ImageTk, Image
from threading import Thread
import io
import sys
import subprocess
import labeler
import gps_get_coords
from uuid import getnode as get_mac

win = Tkinter.Tk()
IniReq = 0
SnapshotReq = 1
ReQuest = IniReq
PlantType = 0 # 1 - Apple, 2 - Corn etc in alphabetical order
# Programmed: Apple,                          Corn,           Grape, Peach, Pepper, Potato,                 Strawberry, Tomato
# Plant list: Apple, Banana, Cabbage, Cherry, Corn, Cucumber, Grape, Peach, Pepper, Potato, Soybean, Sqash, Strawberry, Tomato
buttonPressed = 0
YesNoVal = 128
appdir = '/home/pi/Desktop/PlantCloud/PlantCloud/app'
pathdir = '/home/pi/Desktop/PlantCloud/PlantCloud/'
btnlist = list()
buttonVal = 128

def on_closing():
	if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
		win.destroy()

def exitProgram():
	print("Exit Button pressed")
	win.quit()

def runApple():
	global PlantType
	global buttonPressed
	buttonPressed = 1
	PlantType = 1
	print 'Apple was pressed'

def runCorn():
	global PlantType
	global buttonPressed
	buttonPressed = 1
	PlantType = 2
	print 'Corn was pressed'

def runGrape():
	global PlantType
	global buttonPressed
	buttonPressed = 1
	PlantType = 3
	print 'Grape was pressed'

def runPeach():
	global PlantType
	global buttonPressed
	buttonPressed = 1
	PlantType = 4
	print 'Peach was pressed'

def runPepper():
	global PlantType
	global buttonPressed
	buttonPressed = 1
	PlantType = 5
	print 'Pepper bell was pressed'

def runPotato():
	global PlantType
	global buttonPressed
	buttonPressed = 1
	PlantType = 6
	print 'Potato was pressed'

def runStrawberry():
	global PlantType
	global buttonPressed
	buttonPressed = 1
	PlantType = 7
	print 'Strawberry was pressed'

def runTomato():
	global PlantType
	global buttonPressed
	buttonPressed = 1
	PlantType = 8
	print 'Tomato was pressed'

def runModel():
	print 'Model is running'
	global PlantType
	if PlantType == 1:
		plant = 'apple'
	elif PlantType == 2:
		plant = 'corn'
	elif PlantType == 3:
		plant = 'grape'
	elif PlantType == 4:
		plant = 'peach'
	elif PlantType == 5:
		plant = 'pepper'
	elif PlantType == 6:
		plant = 'potato'
	elif PlantType == 7:
		plant = 'strawberry'
	elif PlantType == 8:
		plant = 'tomato'
	graph = pathdir + 'models/' + plant + '/output_graph.pb'
	labels = pathdir + 'models/' + plant + '/output_labels.txt'
	image = pathdir + 'app/tmp.jpg'
	bestMatch, bestFraction = labeler.label_image(image,labels,graph)
	return bestMatch,bestFraction

def YesNo(value):
	global YesNoVal
	global buttonPressed
	buttonPressed = 1
	YesNoVal = value

def sendYesToServer(bestMatch,bestFraction,imagePath):
	lat,lon = gps_get_coords.get_gps_coords()
	print lat
	print lon
	print get_mac()
	print("Sending info")

def sendNoToServer(imagePath):
	global buttonVal
	lat,lon = gps_get_coords.get_gps_coords()
	print lat
	print lon
	print get_mac()
	print("Sending info")

def btnresponse(value):
	global buttonPressed
	global buttonVal
	buttonPressed = 1
	buttonVal = value
	print value

def confirmNo(imagePath):
	global btnlist
	global PlantType
	global buttonPressed
	global YesNoVal
	if PlantType == 1:
		plant = 'apple'
	elif PlantType == 2:
		plant = 'corn'
	elif PlantType == 3:
		plant = 'grape'
	elif PlantType == 4:
		plant = 'peach'
	elif PlantType == 5:
		plant = 'pepper'
	elif PlantType == 6:
		plant = 'potato'
	elif PlantType == 7:
		plant = 'strawberry'
	elif PlantType == 8:
		plant = 'tomato'
	print("Lookup in "+plant+" dir.")
	labelsfile = open(pathdir+'/models/'+plant+'/output_labels.txt')
	labels = labelsfile.readlines()
	buttonPressed = 0
	textConfirmNoSend = Tkinter.Label(win,text="OK, which one of the following is a good candidate?")
	textConfirmNoSend.pack()
	for line in labels:
		labelThis = line.split('\n')[0]
		btnlist.append(Tkinter.Button(win,text=labelThis,command=lambda labelThis=labelThis: btnresponse(labelThis)))
		btnlist[-1].pack(side=Tkinter.LEFT)
	while not buttonPressed:
		time.sleep(0.1)
	for buttons in btnlist:
		buttons.destroy()
	textConfirmNoSend.destroy()
	textConfirmation = Tkinter.Label(win,text="You selected: "+buttonVal+" Are you sure?")
	textConfirmation.pack()
	yesButton = Tkinter.Button(win,text="Yes",command=lambda *args: YesNo(1))
	yesButton.pack()
	noButton  = Tkinter.Button(win,text="No", command=lambda *args: YesNo(0))
	noButton.pack()
	buttonPressed = 0
	while not buttonPressed:
		time.sleep(0.1)
	textConfirmation.destroy()
	yesButton.destroy()
	noButton.destroy()
	if not YesNoVal:
		exitTest = Tkinter.Button(win,test="Sure, exiting.", command=exitProgram)
	elif YesNoVal == 1:
		textConfirmYesSend = Tkinter.Label(win,text="Great! Sending to the server.",font=("Helvetica",18))
		textConfirmYesSend.pack()
		sendNoToServer(imagePath)

def cameraDisplay(): 
	global buttonPressed
	global ReQuest
	tmpfn = 'tmp.jpg'
	subprocess.call('raspistill -n -vf -o tmp.jpg -w 480 -h 300 -t 10',shell=True)
	tmpImg = ImageTk.PhotoImage(Image.open(tmpfn))
	panel = Tkinter.Label(win,image=tmpImg)
	panel.pack(side=Tkinter.TOP)
	while ReQuest != SnapshotReq:
		subprocess.call('raspistill -n -vf -o tmp.jpg -w 480 -h 300 -t 10',shell=True)
		tmpImg2 = ImageTk.PhotoImage(Image.open(tmpfn))
		panel.configure(image=tmpImg2)
		panel.image = tmpImg2
		print("Displayed image")
	subprocess.call('raspistill -n -vf -o tmp.jpg -t 10',shell=True)
	img3 = Image.open(tmpfn)
	img3 = img3.resize((480,300),Image.ANTIALIAS)
	tmpImg3 = ImageTk.PhotoImage(img3)
	panel.configure(image=tmpImg3)
	SnapshotButton["text"] = 'Acquired'
	text = Tkinter.Label(win,text="Please select the plant type")
	text.pack()
	AppleButton = Tkinter.Button(win,text="Apple",command=runApple)
	AppleButton.pack(side=Tkinter.LEFT)
	CornButton = Tkinter.Button(win,text="Corn",command=runCorn)
	CornButton.pack(side=Tkinter.LEFT)
	GrapeButton = Tkinter.Button(win,text="Grape",command=runGrape)
	GrapeButton.pack(side=Tkinter.LEFT)
	PeachButton = Tkinter.Button(win,text="Peach",command=runPeach)
	PeachButton.pack(side=Tkinter.LEFT)
	PepperButton = Tkinter.Button(win,text="Pepper",command=runPepper)
	PepperButton.pack(side=Tkinter.LEFT)
	PotatoButton = Tkinter.Button(win,text="Potato",command=runPotato)
	PotatoButton.pack(side=Tkinter.LEFT)
	StrawberryButton = Tkinter.Button(win,text="Strawberry",command=runStrawberry)
	StrawberryButton.pack(side=Tkinter.LEFT)
	TomatoButton = Tkinter.Button(win,text="Tomato",command=runTomato)
	TomatoButton.pack(side=Tkinter.LEFT)
	while not buttonPressed:
		time.sleep(0.1)
	AppleButton.destroy()
	CornButton.destroy()
	GrapeButton.destroy()
	PeachButton.destroy()
	PepperButton.destroy()
	PotatoButton.destroy()
	StrawberryButton.destroy()
	TomatoButton.destroy()
	text.destroy()
	text2 = Tkinter.Label(win,text="Model running, please wait....",font=("Helvetica",18))
	text2.pack()
	bestMatch,bestFraction = runModel()
	text2.destroy()
	diseaseInfo = 'Detected ' + bestMatch + ' with ' + str(bestFraction) + ' accuracy.'
	diseaseInfo = diseaseInfo + '\nAre you satisfied with the results?'
	textResult = Tkinter.Label(win,text=diseaseInfo,font=("Helvetica",18))
	textResult.pack(side=Tkinter.LEFT)
	buttonPressed = 0
	yesButton = Tkinter.Button(win,text="Yes",command=lambda *args: YesNo(1))
	yesButton.pack()
	noButton  = Tkinter.Button(win,text="No", command=lambda *args: YesNo(0))
	noButton.pack()
	while not buttonPressed:
		time.sleep(0.1)
	buttonPressed = 0
	global YesNoVal
	noButton.destroy()
	yesButton.destroy()
	textResult.destroy()
	imagePath = appdir + '/tmp.jpg'
	if YesNoVal == 1:
		textConfirmYesSend = Tkinter.Label(win,text="Great! Sending to the server.",font=("Helvetica",18))
		textConfirmYesSend.pack()
		sendYesToServer(bestMatch,bestFraction,imagePath);
	elif YesNoVal == 0:
		confirmNo(imagePath)
	time.sleep(10)
	exitProgram()

def startCameraDisplay():
	camThread = Thread(target=cameraDisplay)
	camThread.start()

def Snapshot():
	global ReQuest
	if ReQuest == IniReq:
		SnapshotButton["text"] = 'Acquiring'
		ReQuest = SnapshotReq

win.title("PlantCloud")
win.geometry('800x430')
ButtonQuit = Tkinter.Button(win, text="Quit", command=exitProgram)
ButtonQuit.pack(side = Tkinter.BOTTOM)

SnapshotButton = Tkinter.Button(win, text = "Snapshot", command = Snapshot)
SnapshotButton.pack(side=Tkinter.LEFT)

startCameraDisplay()
win.protocol("WM_DELETE_WINDOW", on_closing)
win.mainloop()
