from multiprocessing.connection import Client
import pandas as pd
import time
address = ('localhost', 6000)
conn = Client(address, authkey=b'secret password')

csv_file_path = "distanceFile.csv"
df = pd.read_csv(csv_file_path)

visited = {}						#fix this bug

def findNearestNeighbour(currentCityId , j):
	
	dist = df.loc[currentCityId,"dist1":"dist10"]
	print(dist)

	min = 9999
	for i in range(len(dist)):
		if(dist[i] < min and dist[i] != 0):
			if(dist[i] not in visited):				#it still go inside,even if city is visited
				min = dist[i]
				cityIndex = i + 1
	print("min is " , min , "index is " , cityIndex)

	visited[j] = cityIndex
	print("visited is " , visited)
	j+=1
	return cityIndex

#print (df)
j=0
while (j < 10):
	agent1_state = str(conn.recv())
	agent2_state = str(conn.recv())
	print("states are ",agent1_state + " " , agent2_state)
	goToCity = findNearestNeighbour(int(agent1_state) , j)
	
	#msg = input("say something ")
	conn.send(goToCity)

	time.sleep(5)
	j += 1

conn.close()






























