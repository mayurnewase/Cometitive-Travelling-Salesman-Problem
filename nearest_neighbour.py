from multiprocessing.connection import Client
import pandas as pd
import time
class nearestNeighbour:
	nearestNeighbourState = 0
	visited = []

	def __init__(self , nearestNeighbourState , visited):
		self.nearestNeighbourState = nearestNeighbourState
		self.visited = visited.copy()

	def findNearestNeighbour(self , currentCityId , visited):
	#find neirest unvisited city to visit
	#input->
		#currentCityId : current city of agent
		#visited : visited array
		csv_file_path = "distanceFileThirty.csv"
		df = pd.read_csv(csv_file_path)	
		dist = df.loc[currentCityId,"dist0":"dist29"]			#fetch distance values for current city
		#print("distance matrix of ",currentCityId , " is \n" ,dist)
		#print("Visited array " , visited)

		toCheck = []			#this array will store all city ids except current city.so agent can visit them.This is important coz distance of city to same city is 0.so agent may select this every time causing infinite loop.
		
		min = 9999
		for cityIndex in range(len(dist)):
			if(dist[cityIndex] != 0):			#remove current city,and also filter unreachable cities(checkout in hyperX->findBestPolicy)
				#min = dist[i]
				#cityIndex = i + 1
				toCheck.append(cityIndex)		#changed
		#print("toCheck array " , toCheck)

		unVisited = []			#this array will contain unvisited cities ids

		for city in toCheck:
			if city not in visited:
				unVisited.append(city)

		if(len(unVisited) == 0):
			return -1

		#print("unVisited array " , unVisited)

		minDist = 9999
		for city in unVisited:			#now find nearest city
			if (dist[city] < minDist):
				minDist = dist[city]
				#print("city equaling to visit" , city)
				cityToVisit = city

		#print("cityToVisit " , cityToVisit)
		#print("====================================")
		return cityToVisit				#return target city to visit

	def driver(self):

		predictedMove = 0
		currentCityId = self.nearestNeighbourState
		#print("pu currentCityId is ",currentCityId)
		#print("pu visited is ",self.visited)
		predictedMove = self.findNearestNeighbour(currentCityId , self.visited)
		
		return predictedMove















