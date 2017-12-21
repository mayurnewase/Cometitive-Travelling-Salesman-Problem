from tkinter import *
import csv
import pandas as pd
import time
import threading
from multiprocessing.connection import Listener



#csv handling-----------------------------------------------------
csv_file_path = "distanceFile.csv"
df = pd.read_csv(csv_file_path)
X_pos = df.x_pos
Y_pos = df.y_pos
id = df.id


#tkinter init-----------------------------------------------------
master = Tk()
w = Canvas(master , width = 600 , height = 600)
w.pack()

#env graphics-----------------------------------------------------

def drawCircle(x , y , r = 9):
	id = w.create_oval(x-r , y-r , x+r , y+r , fill = "blue")
	return id

def drawAxis(width , height):
	w.create_line(0 , 0 , width , 0 , fill = "black" , width = 5)
	w.create_line(0 , 0 , 0 , height , fill = "black" , width = 5)

	i=0
	while(i < width):
		w.create_text(i , 7 , text = i)
		i = i + 50
	i=0
	while(i < height):
		w.create_text(13 , i , text = i)
		i = i + 50



def drawConnectivity(city1_X , city1_Y , city2_X , city2_Y):
	w.create_line(city1_X , city1_Y , city2_X , city2_Y , width = 2 , fill = "green")



for i in range (11):
	drawCircle(X_pos[i] , Y_pos[i])

drawAxis(600 , 600)

for i in id:
	j=i+1
	while (j <11):
		#drawConnectivity(X_pos[i] , Y_pos[i] , X_pos[j] , Y_pos[j])
		j += 1


##Agent graphics--------------------------------------------------------------------------
#cities_id = df.id
#print(cities_id)

agent1_state = 8
agent2_state = 9

def showAgentState(x , y, r = 9):
	id = w.create_oval(x-r , y-r , x+r , y+r , fill = "red")


showAgentState(X_pos[agent1_state] , Y_pos[agent1_state])
showAgentState(X_pos[agent2_state] , Y_pos[agent2_state])

##Agent movement---------------------------------------------------------------------------

def moveToCityId(agentNo , cityId , agent1_state , agent2_state):

	print("Inside function----->")
	print("agent1_state passed is " , agent1_state)
	print("agent2_state passed is " , agent2_state)
	print("city ID passed is" , cityId)
	print("Outside function----->")

	if(agentNo == 1):
		drawCircle(X_pos[agent1_state] , Y_pos[agent1_state])		#make current blue	
		agent1_state = cityId
	elif(agentNo == 2):
		drawCircle(X_pos[agent2_state] , Y_pos[agent2_state])		#make current blue	
		agent2_state = cityId
	
	showAgentState(X_pos[cityId] , Y_pos[cityId])					#make target city red

	return agent1_state , agent2_state
	
print("Current city of agent 1 is" , agent1_state)
print("Current city of agent 2 is" , agent2_state)

master.update()														#IMPORTANT->required for sleep call in tkinter
time.sleep(4)

#agent1_state , agent2_state = moveToCityId(1 , 3 , agent1_state , agent2_state)
#agent1_state , agent2_state = moveToCityId(2 , 7 , agent1_state , agent2_state)

print("Final city of agent 1 is" , agent1_state)
print("Final city of agent 2 is" , agent2_state)

def initServer():
	print("Starting server")
	address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
	listener = Listener(address, authkey=b'secret password')

	#address2 = ("localhost" , 7000)
	#listener2 = Listener(address2 , authkey = b'password')

	conn = listener.accept()
	#conn2 = listener2.accept()

	print ('connection accepted from listener', listener.last_accepted)
	#print ('connection accepted from listener2', listener2.last_accepted)

	return conn

def acceptNextMoveAgent1(conn , agent1_state , agent2_state):
	
	msg = conn.recv()
	msg = str(msg)
	print("Agent 1 going to " + msg)

	agent1_state , agent2_state = moveToCityId(1 , int(msg) , agent1_state , agent2_state)
	
	return agent1_state , agent2_state

def acceptNextMoveAgent2(conn2):

	msg = conn2.recv()
	msg = str(msg)
	print("Agent 2 going to " + msg)
	agent1_state , agent2_state = moveToCityId(1 , int(msg) , agent1_state , agent2_state)

	return agent1_state , agent2_state

conn = initServer()

while True:
	print("initial agent1_state is " , agent1_state)
	print("initial agent2_state is " , agent2_state)

	msg = conn.recv()
	msg = str(msg)
	print("Agent 1 going to " + msg)

	agent1_state , agent2_state = moveToCityId(1 , int(msg) , agent1_state , agent2_state)

	print("new agent1_state is " , agent1_state)
	print("new agent2_state is " , agent2_state)
	print("-----------------------------------------------")

	master.update()
#agent1_state , agent2_state =  acceptNextMoveAgent1(conn , agent1_state , agent2_state)

#agent1_state , agent2_state = agent1_state , agent2_state
#acceptNextMoveAgent2(conn2 , agent1_state , agent2_state)













#No threading -> coz tkinter is not threadsafe

#t1 = threading.Thread(target = acceptNextMoveAgent1 ,args = [conn , agent1_state , agent2_state])
#t2 = threading.Thread(target = acceptNextMoveAgent2 , args = [conn2])
#t1.daemon = True
#t2.daemon = True
#t1.start()
#t2.start()
#t1.join()
#t2.join()













mainloop()
























