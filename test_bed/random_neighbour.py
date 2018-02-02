from random import randint
from multiprocessing.connection import Client
import pandas as pd


class randomClass:

	csv_file_path = "distanceFileTen.csv"
	df = pd.read_csv(csv_file_path)
	address =0
	conn = 0

	def connectToEnvironment(self , port):
		#AGENT NUMBER DEPENDENT
		#print(randint(0,2))			#give random number --> both inclusive
		self.address = ('localhost', port)
		self.conn = Client(self.address, authkey=b'secret password')


	def random_neighbour(self , currentCityId , visited):
		toCheck = []
		unVisited = []
		random_number = 0
		newCity = 0

		dist = self.df.loc[currentCityId,"dist0":"dist10"]
		print("distance matrix of ",currentCityId , " is \n" ,dist)

		for cityIndex in range(len(dist)):
			if(dist[cityIndex] != 0):
				toCheck.append(cityIndex)

		print("toCheck array is ",toCheck)

		for city in toCheck:
			if city not in visited:
				unVisited.append(city)

		print("unVisited array is ",unVisited)
		if(len(unVisited) == 1):
			flagToStop = True
		else:
			flagToStop = False

		random_number = randint(0 , len(unVisited) - 1)				#both inclusive

		newCity = unVisited[random_number]
		print("new city selected is ",newCity)
		return newCity , flagToStop

	def driver(self):

		visited = []
		initialStateAdded = False
		flagToStop = False
		
		while(not flagToStop):
			print("flag is ",flagToStop)
			agent1_state = str(self.conn.recv())
			print("Current state of random N is " , agent1_state)
			agent2_state = str(self.conn.recv())
			visited = self.conn.recv()
			agent1_target = 0
			#if(initialStateAdded == False):
			#	visited.append(int(agent1_state))
			#	initialStateAdded = True

			toCheck = []
			unVisited = []
			#AGENT NUMBER DEPENDENT
			newCity , flagToStop = self.random_neighbour(int(agent2_state) , visited)

			#visited.append(newCity)
			agent1_target = str(self.conn.recv())
			self.conn.send(newCity)
			
			print("visited array is ",visited)

			input("")

		self.conn.close()
















