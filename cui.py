from tkinter import *
from tkinter import filedialog
import subprocess
import pandas as pd
#from environment import env
#import controller

master =Tk()
filename = StringVar()
randomVar = IntVar()
heuristicVar = StringVar()
positionVar1 = StringVar()
positionVar2 = StringVar()
resultVar1 = StringVar()
resultVar2 = StringVar()


def openFile():
	filename.trace("w",showVarStatus)
	chosenFile = filedialog.askopenfilename(initialdir = "/home/Desktop/project/modularized" , title = "Select csv" , filetypes = (("csv files","*.csv"),("all files","*.*")))
	print("choosen file name is",chosenFile)
	filename.set(chosenFile)
	

def showVarStatus(*args):
	print(filename.get())
	print(randomVar.get())
	print(heuristicVar.get())
	print(positionVar1.get() , " " , positionVar2.get())
	print(resultVar1.get() , " " , resultVar2.get())

def runModules():
	#e = env(filename.get() , int(positionVar1.get()) , int(positionVar2.get()))
	#init(filename.get())
	#sys.argv = [filename.get() , positionVar1.get() , positionVar2.get()]
	sys.argv = ["/home/mayur/Desktop/project/modularized/distanceFileTen.csv", "1", "1"]
	#exec(open("environment.py").read())
	process = subprocess.Popen(["python","environment.py",filename.get(), positionVar1.get(), positionVar2.get()], stdout=subprocess.PIPE)
	#stdout, stderr = p.communicate()
	#print(stdout)
	'''
	while True:
		output = process.stdout.readline()
		if output == b'' and process.poll() is not None:
			break
		if output:
			print (output.strip())
	rc = process.poll()
	'''
	print("BELOW ENVIRONMENT")
	#exec(open("controller.py").read())
	#p = subprocess.Popen(["python","controller.py","/home/mayur/Desktop/project/modularized/distanceFileTen.csv", "5", "2"], stdout=subprocess.PIPE)

def runController():
	p = subprocess.Popen(["python","controller.py",filename.get(), heuristicVar.get()], stdout=subprocess.PIPE)
	stdout = p.communicate()[0]
	#print("result is ")
	print(stdout)

def showResult():
	df = pd.read_csv("finalResult.csv")
	score1 = df["agent1"].iloc[-1]
	score2 = df["agent2"].iloc[-1]
	resultVar1.set(score1)
	resultVar2.set(score2)

def showGraph():
	p = subprocess.Popen(["python" , "plotter.py"])

Label(master, text='Python').pack(side = TOP,pady=10)

#select file
b = Button(master , text = "Select file" , command=openFile).pack()

#checkbox
Checkbutton(master , text = "generate randomly" , variable = randomVar).pack()
randomVar.trace('w' , showVarStatus)

#dropdown
Label(master, text='choose heuristic').pack(side = TOP,pady=10)
choices = {"nn" , "an" , "rn" , "2-opt"}
OptionMenu(master , heuristicVar , *choices).pack()
heuristicVar.trace('w' , showVarStatus)

#position
Label(master, text='initial positions').pack(side = TOP,pady=10)
e1 = Entry(master , textvariable = positionVar1).pack()
e2 = Entry(master, textvariable = positionVar2).pack()
positionVar1.trace("w" , showVarStatus)
positionVar2.trace("w" , showVarStatus)

#run button
b = Button(master , text = "run it" , command=runModules).pack(pady = 10)
b = Button(master , text = "run it" , command=runController).pack(pady = 10)

#result
#Label(master, text='result').pack(side = TOP,pady=10)
b = Button(master , text = "show result" , command = showResult).pack(pady = 10)
e3 = Entry(master , textvariable = resultVar1).pack()
e4 = Entry(master , textvariable = resultVar2).pack()
resultVar1.trace("w" , showVarStatus)
resultVar2.trace("w" , showVarStatus)

#see graph
b = Button(master , text = "Show graph",command = showGraph).pack(pady = 10)


w = Canvas(master , width = 70 , height = 70)
w.pack()


mainloop()























