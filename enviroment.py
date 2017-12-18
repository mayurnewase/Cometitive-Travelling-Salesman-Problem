from tkinter import *
import csv
import pandas as pd
import time

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

for i in range (11):
	drawCircle(X_pos[i] , Y_pos[i])

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

drawAxis(600 , 600)


def drawConnectivity(city1_X , city1_Y , city2_X , city2_Y):
	w.create_line(city1_X , city1_Y , city2_X , city2_Y , width = 2 , fill = "green")


for i in id:
	j=i+1
	while (j <11):
		#drawConnectivity(X_pos[i] , Y_pos[i] , X_pos[j] , Y_pos[j])
		j += 1

##Agent graphics--------------------------------------------------------------------------
cities_id = df.id
#print(cities_id)

agent1_state = 8
agent2_state = 9

def showAgentState(x , y, r = 9):
	id = w.create_oval(x-r , y-r , x+r , y+r , fill = "red")

showAgentState(X_pos[agent1_state] , Y_pos[agent1_state])
showAgentState(X_pos[agent2_state] , Y_pos[agent2_state])

##Agent movement---------------------------------------------------------------------------

def moveToCityId(agentNo , cityId , agent1_state , agent2_state):

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

agent1_state , agent2_state = moveToCityId(1 , 3 , agent1_state , agent2_state)
agent1_state , agent2_state = moveToCityId(2 , 7 , agent1_state , agent2_state)

print("Final city of agent 1 is" , agent1_state)
print("Final city of agent 2 is" , agent2_state)











mainloop()
