from multiprocessing.connection import Client
import pandas as pd
import time
address = ('localhost', 7000)
conn = Client(address, authkey=b'password')

csv_file_path = "distanceFile.csv"
df = pd.read_csv(csv_file_path)


def findNearestNeighbour(currentCityId , visited):
	
	dist = df.loc[currentCityId,"dist0":"dist10"]
	print("distance matrix of ",currentCityId , " is \n" ,dist)
	
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

	minDist = 9999
	for city in unVisited:
		if (dist[city] < minDist):
			minDist = dist[city]
			print("city equaling to visit" , city)
			cityToVisit = city

	print("cityToVisit " , cityToVisit)
	print("====================================")
	return cityToVisit

#print (df)
j=0
visited = []
initialStateAdded = False
while (len(visited) <= 11):
	agent1_state = str(conn.recv())
	agent2_state = str(conn.recv())

	print("agent1_state recieved is ",agent1_state)
	print("agent2_state recieved is ",agent2_state)
	print("states are ",agent1_state , agent2_state)
	
	if(initialStateAdded == False):
		visited.append(int(agent1_state))
		initialStateAdded = True

	goToCity = findNearestNeighbour(int(agent1_state)  , visited)
	
	visited.append(goToCity)
	
	conn.send(goToCity)
	#time.sleep(7)
	input("")
	j += 1

conn.close()


