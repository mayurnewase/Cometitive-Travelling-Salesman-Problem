from tkinter import *
import csv
import pandas as pd
import time
import threading
from multiprocessing.connection import Listener



#csv handling-----------------------------------------------------
csv_file_path = "distanceFile.csv"
df = pd.read_csv(csv_file_path)	#read csv
X_pos = df.x_pos 				#read x co-ordinates
Y_pos = df.y_pos 				#read y co-ordinates
id = df.id 						#read id of city

#tkinter init-----------------------------------------------------
master = Tk()					#initialize tkinter
w = Canvas(master , width = 600 , height = 600)		#create canvas of size 600*600
w.pack()

#env graphics-----------------------------------------------------

def drawCircle(x , y , r = 9):
	#input->
		#x and y co-ordinates
		#radius of circle

	#output->
		#id of circle created(its not used anywhere right now)
	id = w.create_oval(x-r , y-r , x+r , y+r , fill = "blue")
	return id


for i in range (11):			#draw each city.(co-ordinates stored in X_pos and Y_pos)
	drawCircle(X_pos[i] , Y_pos[i])


def drawAxis(width , height):
	#draw axis (x,y) along 2 sides of canvas
	#also print values at some distance
	#input->
		#width
		#height

	w.create_line(0 , 0 , width , 0 , fill = "black" , width = 5)	#create_line(p1_X , p1_Y , p2_X , p2_Y)
	w.create_line(0 , 0 , 0 , height , fill = "black" , width = 5)

	i=0
	while(i < width):						#to print text at specific distance
		w.create_text(i , 7 , text = i)
		i = i + 50
	i=0
	while(i < height):
		w.create_text(13 , i , text = i)
		i = i + 50

drawAxis(600 , 600)

def drawConnectivity(city1_X , city1_Y , city2_X , city2_Y):
	#draw lines connecting cities
	#input->
		#x and y co-ordinates of both cities
		
	w.create_line(city1_X , city1_Y , city2_X , city2_Y , width = 2 , fill = "green")



for i in id:		#draw connectivity
	j=i+1
	while (j <11):
		#drawConnectivity(X_pos[i] , Y_pos[i] , X_pos[j] , Y_pos[j])
		j += 1


##Agent graphics--------------------------------------------------------------------------
#cities_id = df.id
#print(cities_id)

agent1_state = 8	#take initial states of agents
agent2_state = 9

def showAgentState(x , y, r = 9):
	#show cirrent agent states in canvas by changing color of cities
	#this basically create new circle over existing city with different color.
	#coz we cant change only color of already drawn circle

	id = w.create_oval(x-r , y-r , x+r , y+r , fill = "red")


showAgentState(X_pos[agent1_state] , Y_pos[agent1_state])
showAgentState(X_pos[agent2_state] , Y_pos[agent2_state])

##Agent movement---------------------------------------------------------------------------

def moveToCityId(agentNo , cityId , agent1_state , agent2_state):
	#move the agent to different city
	#make current city back to normal color(to show agent has left)
	#and change target city's color different(to show agents current position)

	#input->
		#agentNo : which agent to move(1st or 2nd)
		#cityId : which city to visit(target city)
		#agent1_state,agent2_state : current states of both agent.(states before visiting new city)
	#output->
		#new states of both agents

	if(agentNo == 1):
		drawCircle(X_pos[agent1_state] , Y_pos[agent1_state])		#make current blue	
		agent1_state = cityId 										#update state
	elif(agentNo == 2):
		drawCircle(X_pos[agent2_state] , Y_pos[agent2_state])		#make current blue	
		agent2_state = cityId 										#update state
	
	showAgentState(X_pos[cityId] , Y_pos[cityId])					#make target city red

	return agent1_state , agent2_state
	
print("Current city of agent 1 is" , agent1_state)
print("Current city of agent 2 is" , agent2_state)

def showInitialAgentData():
	#w.create_text(500 , 25 , text="Agent 1 benifit\nAgent 2 benifit")
	T = Text(master, height=2, width=30)
	T.pack()
	T.insert(END, "Agent 1 benifit : 0 \nAgent 2 benifit : 0\n")
	#T.delete("1.18" , "1.20")
	#T.insert('1.19' , 20)

	#T.insert('1.19' , 234)
	#T.delete('1.17' , '1.19')
	return T

T = showInitialAgentData()

def updateAgentData(benifit):

	T.delete("1.18" , "1.20")
	T.delete("2.18" , "2.20")
	T.insert('1.19' , benifit[0])
	T.insert('2.19' , benifit[1])
	master.update()



master.update()								#IMPORTANT->required for sleep call in tkinter

#time.sleep(4)
#agent1_state , agent2_state = moveToCityId(1 , 3 , agent1_state , agent2_state)
#agent1_state , agent2_state = moveToCityId(2 , 7 , agent1_state , agent2_state)

#print("Final city of agent 1 is" , agent1_state)
#print("Final city of agent 2 is" , agent2_state)



def initServer():
	#create 2 listeners that accepts outputs from external agent programmes.
	#2 listeners are on different addresses
	#output->
		#2 connections from both agents

	print("Starting server")
	address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
	listener = Listener(address, authkey=b'secret password')

	address2 = ("localhost" , 7000)
	listener2 = Listener(address2 , authkey = b'password')

	conn = listener.accept()
	conn2 = listener2.accept()

	print ('connection accepted from listener', listener.last_accepted)
	#print ('connection accepted from listener2', listener2.last_accepted)

	return conn , conn2

def giveInfoToAgent(conn , conn2 ,agent1_state , agent2_state , visited):
	#give info back to both agents.
	#info includes current states of both agents

	conn.send(agent1_state)
	conn.send(agent2_state)
	conn.send(visited)

	conn2.send(agent1_state)
	conn2.send(agent2_state)
	conn2.send(visited)

conn , conn2 = initServer()


	

visited = []
benifit = [0] * 2

visited.append(agent1_state)
visited.append(agent2_state)

print("initial agent1_state is " , agent1_state)
print("initial agent2_state is " , agent2_state)
prev1_state = agent1_state
prev2_state = agent2_state

while True:
	
	giveInfoToAgent(conn , conn2 , agent1_state , agent2_state , visited)	#send info to agents

	msg = conn.recv()			#get move from agent1
	msg = str(msg)
	print("Agent 1 going to " + msg)
	
	conn2.send(int(msg))			#Give agent 1 target city to aggressive agent

	msg2 = conn2.recv()			#get move from agent2
	msg2 = str(msg2)
	print("Agent 2 going to " + msg2)

	agent1_state , agent2_state = moveToCityId(1 , int(msg) , agent1_state , agent2_state)
	agent1_state , agent2_state = moveToCityId(2 , int(msg2) , agent1_state , agent2_state)
	print("new agent1_state is " , agent1_state)
	print("new agent2_state is " , agent2_state)
	print("-----------------------------------------------")

	if(agent1_state != agent2_state):
		benifit[0] += 1
		benifit[1] += 1

	else:
		df2 = df.loc[prev1_state , "dist0":"dist10"]
		cost1 = df2[agent1_state]
		print("Agent 1 transition cost " , cost1)

		df2 = df.loc[prev2_state , "dist0":"dist10"]
		cost2 = df2[agent2_state]
		print("Agent 2 transition cost " , cost2)

		if(cost1 < cost2):
			benifit[0] += 1
		else:
			benifit[1] += 1

	updateAgentData(benifit)
	visited.append(agent1_state)
	visited.append(agent2_state)

	prev1_state = agent1_state
	prev2_state = agent2_state


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

mainloop()		#important for tkinter to persist till end of program