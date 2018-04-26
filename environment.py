from tkinter import *
import csv
import pandas as pd
import time
import threading
from multiprocessing.connection import Listener
from csvWriter import logWriter
from random import randint

print(b"in environment")
print(sys.argv[0] , sys.argv[1],sys.argv[2])
#csv handling-----------------------------------------------------
#class env:
#def __init__(self,csv_file_path_recieved , agent1_state_recieved , agent2_state_recieved):
	#initVariables(csv_file_path_recieved , agent1_state_recieved , agent2_state_recieved)
#global csv_file_path , df , X_pos , Y_pos , id , agent1_state , agent2_state
global ids , df , X_pos , Y_pos , agent1_state , agent2_state
csv_file_path = str(sys.argv[1])
df = pd.read_csv(csv_file_path)	#read csv
X_pos = df.x_pos 				#read x co-ordinates
print(X_pos)
Y_pos = df.y_pos 				#read y co-ordinates
ids = df.id 						#read id of city

agent1_state = int(sys.argv[2])	#take initial states of agents
agent2_state = int(sys.argv[3])
print("HEY I AM IN ENVIRONMENT")
#self.runAll()
#def initVariables(self,csv_file_path_recieved , agent1_state_recieved , agent2_state_recieved):#call
	
def tkInit():#call
	global master , w
	#tkinter init-----------------------------------------------------
	master = Tk()					#initialize tkinter
	w = Canvas(master , width = 600 , height = 600)		#create canvas of size 600*600
	w.pack()

#env graphics-----------------------------------------------------

def drawCircle(x , y , r = 4):
	#input->
		#x and y co-ordinates
		#radius of circle

	#output->
		#id of circle created(its not used anywhere right now)
	id = w.create_oval(x-r , y-r , x+r , y+r , fill = "blue")
	return id

def drawCities():#call
	global drawCircle
	print(len(ids))
	for i in range (len(ids)):			#draw each city.(co-ordinates stored in X_pos and Y_pos)
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

#drawAxis(600 , 600)#call

def drawConnectivity(city1_X , city1_Y , city2_X , city2_Y):
	#draw lines connecting cities
	#input->
		#x and y co-ordinates of both cities
		
	w.create_line(city1_X , city1_Y , city2_X , city2_Y , width = 2 , fill = "green")

def drawPaths():#call

	for i in ids:		#draw connectivity
		j=i+1
		while (j <11):
			#drawConnectivity(X_pos[i] , Y_pos[i] , X_pos[j] , Y_pos[j])
			j += 1


##Agent graphics--------------------------------------------------------------------------
#cities_id = df.id
#print(cities_id)

#agent1_state = 2	#take initial states of agents
#agent2_state = 7

def showAgentState(x , y, r = 9):
	#show cirrent agent states in canvas by changing color of cities
	#this basically create new circle over existing city with different color.
	#coz we cant change only color of already drawn circle
	print("showAgentState ",x , " ",y)
	id = w.create_oval(x-r , y-r , x+r , y+r , fill = "red")


#showAgentState(X_pos[agent1_state] , Y_pos[agent1_state])
#showAgentState(X_pos[agent2_state] , Y_pos[agent2_state])

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
	
#print("Current city of agent 1 is" , agent1_state)
#print("Current city of agent 2 is" , agent2_state)

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

#T = showInitialAgentData()

def updateAgentData(benifit):

	T.delete("1.18" , "1.20")
	T.delete("2.18" , "2.20")
	T.insert('1.19' , benifit[0])
	T.insert('2.19' , benifit[1])
	master.update()



#master.update()								#IMPORTANT->required for sleep call in tkinter

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
	global Listener

	print("Starting server")
	address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
	listener = Listener(address, authkey=b'secret password')

	address2 = ("localhost" , 7000)
	listener2 = Listener(address2 , authkey = b'secret password')

	conn = listener.accept()
	print ('connection accepted from listener', listener.last_accepted)
	conn2 = listener2.accept()
	print ('connection accepted from listener2', listener2.last_accepted)

	return conn , conn2

def giveInfoToAgent(conn , conn2 ,agent1_state , agent2_state , visited):
	#give info back to both agents.
	#info includes current states of both agents
	conn.send(agent1_state)
	conn.send(agent2_state)
	conn.send(visited)


#def runAll(self):
#	global csv_file_path , df , X_pos , Y_pos , ids , agent1_state , agent2_state

tkInit()
drawCities()
drawAxis(600 , 600)
drawPaths()
showAgentState(X_pos[agent1_state] , Y_pos[agent1_state])
showAgentState(X_pos[agent2_state] , Y_pos[agent2_state])

print("Current city of agent 1 is" , agent1_state)
print("Current city of agent 2 is" , agent2_state)
master.update()

conn , conn2 = initServer()

#All log values initializing............
otherAgentHeuristic = conn2.recv()					#to write logs in csv
otherAgentHeuristic = str(otherAgentHeuristic)
agent1_state_for_logs = agent1_state
agent2_state_for_logs = agent2_state

visited = []
benifit = [0] * 2
costOfTravel = [0] * 2
finalCostToSubstractForLastCity1 = 0
finalCostToSubstractForLastCity2 = 0

visited.append(agent1_state)
visited.append(agent2_state)

print("initial agent1_state is " , agent1_state)
print("initial agent2_state is " , agent2_state)
prev1_state = agent1_state
prev2_state = agent2_state
i = 1				#index to skip accepting info from agents per 3 steps

repeatingStateCounter = 0
flagShuffle = False
while True:

	giveInfoToAgent(conn , conn2 , agent1_state , agent2_state , visited)	#send info to agents
	flagShuffle = False
	print("skipping index is ",i)

	if(i%4 == 0):
		i = 1
		continue
	i += 1
	
	msg = conn.recv()			#get move from agent1
	msg = str(msg)
	print("Agent 1 going to " + msg)
	
	#conn2.send(int(msg))			#Give agent 1 target city to aggressive agent

	msg2 = conn2.recv()			#get move from agent2
	msg2 = str(msg2)
	print("Agent 2 going to " + msg2)

	if(int(msg) == -1 or int(msg2) == -1):
		conn.close()
		conn2.close()
		break
	#conn.send(int(msg2))
	if(int(msg) == int(msg2)):
		repeatingStateCounter += 1
	if(repeatingStateCounter == 2):
		flagShuffle = True
		repeatingStateCounter = 0

	agent1_state , agent2_state = moveToCityId(1 , int(msg) , agent1_state , agent2_state)
	agent1_state , agent2_state = moveToCityId(2 , int(msg2) , agent1_state , agent2_state)
	print("new agent1_state is " , agent1_state)
	print("new agent2_state is " , agent2_state)
	
	finalCostToSubstractForLastCity1 = 0
	finalCostToSubstractForLastCity2 = 0

	if(agent1_state != agent2_state):
		if(agent1_state not in visited):
			benifit[0] += 500
			finalCostToSubstractForLastCity1 = 500

		if(agent2_state not in visited):
			benifit[1] += 500
			finalCostToSubstractForLastCity2 = 500

		df2 = df.loc[prev1_state , "dist0":"dist" + str(len(ids) - 1)]
		cost1 = df2[agent1_state]
		print("Agent 1 transition cost " , cost1)

		df2 = df.loc[prev2_state , "dist0":"dist" + str(len(ids) - 1)]
		cost2 = df2[agent2_state]
		print("Agent 2 transition cost " , cost2)

	else:

		df2 = df.loc[prev1_state , "dist0":"dist" + str(len(ids) - 1)]
		cost1 = df2[agent1_state]
		print("Agent 1 transition cost " , cost1)

		df2 = df.loc[prev2_state , "dist0":"dist" + str(len(ids) - 1)]
		cost2 = df2[agent2_state]
		print("Agent 2 transition cost " , cost2)

		if(cost1 < cost2):
			benifit[0] += 500
			finalCostToSubstractForLastCity1 = 500
			#finalCostToSubstractForLastCity2 = 0
		elif(cost1 > cost2):
			benifit[1] += 500
			finalCostToSubstractForLastCity2 = 500
			#finalCostToSubstractForLastCity1 = 0
		elif(cost1 == cost2):	#sharing benifit
			benifit[0] += 250
			benifit[1] += 250
			finalCostToSubstractForLastCity1 = 250
			finalCostToSubstractForLastCity2 = 250


	df2 = df.loc[prev1_state , "dist0":"dist" + str(len(ids) - 1)]
	cost1 = df2[agent1_state]
	costOfTravel[0] += cost1

	df2 = df.loc[prev2_state , "dist0":"dist" + str(len(ids) - 1)]
	cost2 = df2[agent2_state]
	costOfTravel[1] += cost2

	#updateAgentData(benifit)
	visited.append(agent1_state)
	visited.append(agent2_state)

	prev1_state = agent1_state
	prev2_state = agent2_state
	print("\n Benifit vector is ")
	print(benifit)
	print("Cost of travel vector is ")
	print(costOfTravel)
	print("if ended here cost substracted is ",finalCostToSubstractForLastCity1 , " ",finalCostToSubstractForLastCity2)
	print("-----------------------------------------------")

	master.update()
	#agent1_state , agent2_state =  acceptNextMoveAgent1(conn , agent1_state , agent2_state)
	#agent1_state , agent2_state = agent1_state , agent2_state
	#acceptNextMoveAgent2(conn2 , agent1_state , agent2_state)

print("\nFinal values are")
print("Total benifits are ",benifit)
print("Total costs for travelling are ",costOfTravel)

unvisited=[]
for i in range(len(ids)):
	if i not in visited:
		unvisited.append(i)

print("leftover unvisited is ",unvisited)

if(len(unvisited) == 1):
	df2 = df.loc[agent1_state , "dist0":"dist" + str(len(ids) - 1)]
	cost1 = df2[unvisited[0]]
	df2 = df.loc[agent2_state , "dist0":"dist" + str(len(ids) - 1)]
	cost2 = df2[unvisited[0]]

	finalCostToSubstractForLastCity1 = cost1
	finalCostToSubstractForLastCity2 = cost2

print("fianl cities cost to substract are ",finalCostToSubstractForLastCity1 , " ",finalCostToSubstractForLastCity2)
finalBenifit_1 = benifit[0] - costOfTravel[0] - finalCostToSubstractForLastCity1
finalBenifit_2 = benifit[1] - costOfTravel[1] - finalCostToSubstractForLastCity2

print("Final benifits are")
print("Agent 1 benifit : " , finalBenifit_1)
print("Agent 2 benifit : " , finalBenifit_2)

lg = logWriter(agent1_state_for_logs , agent2_state_for_logs , otherAgentHeuristic , finalBenifit_1 , finalBenifit_2)
lg.write()









#No threading -> coz tkinter is not threadsafe

#t1 = threading.Thread(target = acceptNextMoveAgent1 ,args = [conn , agent1_state , agent2_state])
#t2 = threading.Thread(target = acceptNextMoveAgent2 , args = [conn2])
#t1.daemon = True
#t2.daemon = True
#t1.start()
#t2.start()
#t1.join()
#t2.join()
exit()
mainloop()		#important for tkinter to persist till end of program
