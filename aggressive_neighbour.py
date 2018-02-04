from multiprocessing.connection import Client
import pandas as pd
import time
address = ('localhost', 6000)
conn = Client(address, authkey=b'secret password')

csv_file_path = "distanceFile.csv"
df = pd.read_csv(csv_file_path)


def findNearestNeighbour(currentCityId , visited):
	
	dist = df.loc[currentCityId,"dist0":"dist10"]
	print("distance matrix of ", currentCityId , " is \n" ,dist)
	
	print("Visited array " , visited)
	toCheck = []
	min = 9999
	for cityIndex in range(len(dist)):
		if(dist[cityIndex] != 0):			#remove current city.
			#min = dist[i]
			#cityIndex = i + 1
			toCheck.append(cityIndex)		#changed
	print("toCheck array " , toCheck)

	unVisited = []

	for city in toCheck:
		if city not in visited:
			unVisited.append(city)

	print("unVisited array " , unVisited)
	
	if(len(unVisited) == 0):
		return -1

	minDist = 9999
	for city in unVisited:
		if (dist[city] < minDist):
			minDist = dist[city]
			print("city equaling to visit" , city)
			cityToVisit = city

	#print("cityToVisit " , cityToVisit)
	print("====================================")
	return cityToVisit

#print (df)
j=0
visited = []
initialStateAdded = False
nearestCity = 0
while (nearestCity != -1):
	agent1_state = str(conn.recv())
	agent2_state = str(conn.recv())
	visited = conn.recv()
	agent1_target = str(conn.recv())

	print("agent1_state recieved is ",agent1_state)
	print("agent2_state recieved is ",agent2_state)
	print("states are ",agent1_state , agent2_state)
	
	#if(initialStateAdded == False):
		#visited.append(int(agent1_state))
		#initialStateAdded = True

	nearestCity = findNearestNeighbour(int(agent1_state)  , visited)	#AGENT NO DEPENDENT
	#visited.append(goToCity)
	if(nearestCity == -1):
		break
	print("found nearestCity ",nearestCity)
	#cost for agent 2 current state -> nearest neighbour
	row_data = df.loc[int(agent2_state) , "dist0":"dist10"]
	cost1 = row_data[nearestCity]
	print("agent 2 current state [",agent2_state  , "] -> nearest neighbour [",nearestCity,"]" , cost1)

	#cost for agent 2's current state -> agent 1's target city
	row_data = df.loc[int(agent2_state) , "dist0":"dist10"]
	cost2 = row_data[int(agent1_target)]
	print("agent 2 current state [" , agent2_state ,"] -> agent 1's target [",agent1_target ,"]", cost2)
	
	#cost for agent 1's current state -> agent 1's target city
	row_data = df.loc[int(agent1_state) , "dist0":"dist10"]
	cost3 = row_data[int(agent1_target)]
	print("agent 1 current state [" , agent1_state , "] -> agent 1's target [",agent1_target ,"]", cost3)

	if(agent1_target == agent2_state):	#if other dumbass agent choose target same as current state of this agent,then aggressive will go to nearest city,instead of remaining in current position.
		goToCity = nearestCity
	elif(cost2 < cost3):				#Aggressive agent can reach others target early
		goToCity = agent1_target
		print("Ditching that nigga..... LMAO")
	elif(cost2 >= cost3):
		goToCity = nearestCity
	


	print("Going to " , goToCity)
	conn.send(goToCity)
	print("visited array is ",visited)
	#time.sleep(7)
	input("")
	j += 1

conn.close()






























