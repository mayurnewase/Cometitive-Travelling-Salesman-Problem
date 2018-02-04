from multiprocessing.connection import Client
import pandas as pd
import time
address = ('localhost', 7000)
conn = Client(address, authkey=b'secret password')

csv_file_path = "distanceFile.csv"
df = pd.read_csv(csv_file_path)


def findNearestNeighbour(currentCityId , visited):
	#find neirest unvisited city to visit
	#input->
		#currentCityId : current city of agent
		#visited : visited array
	
	dist = df.loc[currentCityId,"dist0":"dist10"]			#fetch distance values for current city
	print("distance matrix of ",currentCityId , " is \n" ,dist)
	print("Visited array " , visited)

	toCheck = []			#this array will store all city ids except current city.so agent can visit them.This is important coz distance of city to same city is 0.so agent may select this every time causing infinite loop.
	
	min = 9999
	for cityIndex in range(len(dist)):
		if(dist[cityIndex] != 0):			#remove current city.
			#min = dist[i]
			#cityIndex = i + 1
			toCheck.append(cityIndex)		#changed
	print("toCheck array " , toCheck)

	unVisited = []			#this array will contain unvisited cities ids

	for city in toCheck:
		if city not in visited:
			unVisited.append(city)

	print("unVisited array " , unVisited)
	
	if(len(unVisited) == 0):
		return -1

	minDist = 9999
	for city in unVisited:			#now find nearest city
		if (dist[city] < minDist):
			minDist = dist[city]
			#print("city equaling to visit" , city)
			cityToVisit = city

	print("cityToVisit " , cityToVisit)
	print("====================================")
	return cityToVisit				#return target city to visit

#print (df)
j=0				#used for looping counter
visited = []	#store visited cities
initialStateAdded = False	#add initial only for first time
goToCity = 0

while (goToCity != -1):
	agent1_state = str(conn.recv())			#get states from environment
	agent2_state = str(conn.recv())
	visited = conn.recv()

	print("agent1_state recieved is ",agent1_state)
	print("agent2_state recieved is ",agent2_state)
	print("states are ",agent1_state , agent2_state)
	
	#if(initialStateAdded == False):			#add initial state in visited[]
	#	visited.append(int(agent1_state))
	#	initialStateAdded = True

	goToCity = findNearestNeighbour(int(agent2_state)  , visited)	#find target city
	
	#visited.append(goToCity)			#add target city in visited[]
	if(goToCity != -1):
		conn.send(goToCity)
		agent2_target = str(conn.recv())
		#time.sleep(7)
		input("")
		j += 1

conn.close()		#close connection safely






























