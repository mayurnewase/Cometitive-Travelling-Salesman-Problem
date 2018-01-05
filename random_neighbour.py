from random import randint
from multiprocessing.connection import Client
import pandas as pd

#print(randint(0,2))			#give random number --> both inclusive
address = ('localhost', 6000)
conn = Client(address, authkey=b'secret password')

csv_file_path = "distanceFile.csv"
df = pd.read_csv(csv_file_path)


def random_neighbour(currentCityId , visited):

	dist = df.loc[currentCityId,"dist0":"dist10"]
	print("distance matrix of ",currentCityId , " is \n" ,dist)

	for cityIndex in range(len(dist)):
		if(dist[cityIndex] != 0):
			toCheck.append(cityIndex)

	print("toCheck array is ",toCheck)

	for city in toCheck:
		if city not in visited:
			unVisited.append(city)

	print("unVisited array is ",unVisited)

	random_number = randint(0 , len(unVisited) - 1)				#both inclusive

	newCity = unVisited[random_number]
	print("new city selected is ",newCity)
	return newCity

visited = []
initialStateAdded = False

while(len(visited) < 11):
	agent1_state = str(conn.recv())
	agent2_state = str(conn.recv())
	visited = conn.recv()

	#if(initialStateAdded == False):
	#	visited.append(int(agent1_state))
	#	initialStateAdded = True

	toCheck = []
	unVisited = []

	newCity = random_neighbour(int(agent1_state) , visited)

	#visited.append(newCity)

	conn.send(newCity)
	print("visited array is ",visited)

	input("")

conn.close()
















