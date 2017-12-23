from multiprocessing.connection import Client
import pandas as pd
import time
address = ('localhost', 6000)
conn = Client(address, authkey=b'secret password')

csv_file_path = "distanceFile.csv"
df = pd.read_csv(csv_file_path)


def findNearestNeighbour(currentCityId , j , visited):
	
	dist = df.loc[currentCityId,"dist1":"dist10"]
	print(dist)
	
	print("Visited array " , visited)
	toCheck = []
	min = 9999
	for cityIndex in range(len(dist)):
		if(dist[cityIndex] != 0):			#remove current city.
			#min = dist[i]
			#cityIndex = i + 1
			toCheck.append(cityIndex)
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
while (len(visited) < 10):
	agent1_state = str(conn.recv())
	agent2_state = str(conn.recv())
	print("states are ",agent1_state + " " , agent2_state)
	
	if(initialStateAdded == False):
		visited.append(int(agent1_state))
		initialStateAdded = True

	goToCity = findNearestNeighbour(int(agent1_state) , j , visited)
	
	visited.append(goToCity)
	
	conn.send(goToCity)
	time.sleep(7)
	
	j += 1

conn.close()



