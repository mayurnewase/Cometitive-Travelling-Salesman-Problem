from multiprocessing.connection import Client
import pandas as pd
import time
class aggressiveNeighbour:
	aggressiveState = 0
	otherAgentState = 0
	otherAgentTarget = 0

	visited = []
	
	csv_file_path = "distanceFileThirty.csv"
	df = pd.read_csv(csv_file_path)

	def __init__(self , aggressiveState , otherAgentState , otherAgentTarget , visited):
		self.aggressiveState = aggressiveState
		self.visited = visited.copy()
		self.otherAgentState = otherAgentState
		self.otherAgentTarget = otherAgentTarget

	def findNearestNeighbour(self , currentCityId , visited):
		
		dist = self.df.loc[currentCityId,"dist0":"dist29"]
		#print("distance matrix of ", self.state , " is \n" ,dist)
		
		toCheck = []
		min = 9999
		for cityIndex in range(len(dist)):
			if(dist[cityIndex] != 0):			#remove current city.
				#min = dist[i]
				#cityIndex = i + 1
				toCheck.append(cityIndex)		#changed
		#print("toCheck array " , toCheck)

		unVisited = []

		for city in toCheck:
			if city not in visited:
				unVisited.append(city)

		#print("unVisited array " , unVisited)
		if(len(unVisited) == 0):
			return -1

		minDist = 9999
		for city in unVisited:
			if (dist[city] < minDist):
				minDist = dist[city]
				#print("city equaling to visit" , city)
				cityToVisit = city

		#print("cityToVisit " , cityToVisit)
		#print("====================================")
		return cityToVisit

	def driver(self):

		nearestCity = self.findNearestNeighbour(self.aggressiveState  , self.visited)
		if(nearestCity == -1):
			return -1
			
		row_data = self.df.loc[int(self.aggressiveState) , "dist0":"dist29"]
		cost1 = row_data[nearestCity]

		row_data = self.df.loc[int(self.aggressiveState) , "dist0":"dist29"]
		cost2 = row_data[int(self.otherAgentTarget)]

		row_data = self.df.loc[int(self.otherAgentState) , "dist0":"dist29"]
		cost3 = row_data[int(self.otherAgentTarget)]

		if(self.otherAgentTarget == self.aggressiveState):				#if other dumb agent choose target same as current state of this agent,then aggressive will go to nearest city,instead of remaining in current position.
			goToCity = nearestCity
		elif(cost2 < cost3):				#Aggressive agent can reach others target early
			goToCity = self.otherAgentTarget	
			print("Ditching that nigga..... LMAO")
		elif(cost2 >= cost3):
			goToCity = nearestCity

		return goToCity

















