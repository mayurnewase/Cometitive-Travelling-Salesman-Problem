from random import randint
from multiprocessing.connection import Client
import pandas as pd

#print(randint(0,2))			#give random number --> both inclusive

class random:
	
	csv_file_path = "distanceFileThirty.csv"
	df = pd.read_csv(csv_file_path)
	
	thisState = 0
	visited = []

	def __init__(self , thisState , visited):
		self.thisState = thisState
		self.visited = visited

	def random_neighbour(self , currentCityId , visited):

		dist = self.df.loc[currentCityId,"dist0":"dist29"]
		#print("distance matrix of ",currentCityId , " is \n" ,dist)
		toCheck = []
		unVisited = []

		for cityIndex in range(len(dist)):
			if(dist[cityIndex] != 0):
				toCheck.append(cityIndex)

		#print("toCheck array is ",toCheck)

		for city in toCheck:
			if city not in visited:
				unVisited.append(city)

		if(len(unVisited) == 0):
			return -1

		#print("unVisited array is ",unVisited)

		random_number = randint(0 , len(unVisited) - 1)				#both inclusive

		newCity = unVisited[random_number]
		#print("new city selected is ",newCity)
		return newCity

	def driver(self):


		newCity = self.random_neighbour(int(self.thisState) , self.visited)
		return newCity
		







