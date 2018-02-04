from random import randint
import pandas as pd

class nearestNeighbour:
	nearestNeighbourState = 0
	probability = []
	visited = []

	def __init__(self , nearestNeighbourState , probability , visited):
		self.nearestNeighbourState = nearestNeighbourState
		self.probability = probability.copy()
		self.visited = visited.copy()

	def findNearestNeighbour(self , currentCityId , visited):
	#find neirest unvisited city to visit
	#input->
		#currentCityId : current city of agent
		#visited : visited array
		csv_file_path = "distanceFileTen.csv"
		df = pd.read_csv(csv_file_path)	
		dist = df.loc[currentCityId,"dist0":"dist10"]			#fetch distance values for current city
		#print("distance matrix of ",currentCityId , " is \n" ,dist)
		#print("Visited array " , visited)

		toCheck = []			#this array will store all city ids except current city.so agent can visit them.This is important coz distance of city to same city is 0.so agent may select this every time causing infinite loop.
		
		min = 9999
		for cityIndex in range(len(dist)):
			if(dist[cityIndex] != 0):			#remove current city.
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


class aggressiveNeighbour:
	aggressiveState = 0
	otherAgentState = 0
	otherAgentTarget = 0

	probability = []
	visited = []
	
	csv_file_path = "distanceFileTen.csv"
	df = pd.read_csv(csv_file_path)

	def __init__(self , aggressiveState , otherAgentState ,otherAgentTarget ,probability , visited):
		self.aggressiveState = aggressiveState
		self.probability = probability.copy()
		self.visited = visited.copy()
		self.otherAgentState = otherAgentState
		self.otherAgentTarget = otherAgentTarget

	def findNearestNeighbour(self , currentCityId , visited):
		
		dist = self.df.loc[currentCityId,"dist0":"dist10"]
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
		row_data = self.df.loc[int(self.aggressiveState) , "dist0":"dist10"]
		cost1 = row_data[nearestCity]

		row_data = self.df.loc[int(self.aggressiveState) , "dist0":"dist10"]
		cost2 = row_data[int(self.otherAgentTarget)]

		row_data = self.df.loc[int(self.otherAgentState) , "dist0":"dist10"]
		cost3 = row_data[int(self.otherAgentTarget)]

		if(self.otherAgentTarget == self.aggressiveState):				#if other dumb agent choose target same as current state of this agent,then aggressive will go to nearest city,instead of remaining in current position.
			goToCity = nearestCity
		elif(cost2 < cost3):				#Aggressive agent can reach others target early
			goToCity = self.otherAgentTarget	
			print("Ditching that nigga..... LMAO")
		elif(cost2 >= cost3):
			goToCity = nearestCity

		return goToCity


class twoOpt:
	
	twoOptAgentState = 0
	
	csv_file_path = "distanceFileTen.csv"
	df = pd.read_csv(csv_file_path)

	def __init__(self , twoOptAgentState):
		self.twoOptAgentState = twoOptAgentState
		
		
	def findNearestNeighbour(self , currentCityId , visited):
		
		dist = self.df.loc[currentCityId,"dist0":"dist10"]			#fetch distance values for current city
		#print("distance matrix of ",currentCityId , " is \n" ,dist)
		#print("Visited array " , visited)

		toCheck = []			#this array will store all city ids except current city.so agent can visit them.This is important coz distance of city to same city is 0.so agent may select this every time causing infinite loop.
		
		min = 9999
		for cityIndex in range(len(dist)):
			if(dist[cityIndex] != 0):			#remove current and unreachable cities.
				#min = dist[i]
				#cityIndex = i + 1
				toCheck.append(cityIndex)		#changed
		#print("toCheck array " , toCheck)

		unVisited = []			#this array will contain unvisited cities ids

		for city in toCheck:
			if city not in visited:
				unVisited.append(city)

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

	def findCostOfTravel(self , route):
		cost = 0
		for i in range(len(route) - 1):
			row_data = self.df.loc[route[i] , "dist0" : "dist10"]
			if(row_data[route[i + 1]] == 0):					#if there is no path between cities
				return 9999
			cost += row_data[route[i+1]]

		return cost

	def swapper(self , route , startCityIndex , endCityIndex):
		#print("startCity is ",startCityIndex)
		#print("endCity is ",endCityIndex)

		route1 = route.copy()
		route2 = route.copy()

		city0 = route[startCityIndex]
		city1 = route[startCityIndex+1]
		city2 = route[startCityIndex+2]
		city3 = route[startCityIndex+3]
		#print("Cities are  ",city0 , city1 , city2 , city3)
		route1[startCityIndex + 1] = city2			#1 & 2
		route1[startCityIndex + 2] = city1

		route2[startCityIndex + 1] = city3			#1 & 2 & 3
		route2[startCityIndex + 2] = city1
		route2[startCityIndex + 3] = city2

		return route1 , route2

	def driver(self):
		
		predictedPath = []
		initialStateAdded = False

		while (len(predictedPath) < 11):
		
			if(initialStateAdded == False):			#add initial state in visited[]
				predictedPath.append(self.twoOptAgentState)
				initialStateAdded = True

			goToCity = self.findNearestNeighbour(self.twoOptAgentState , predictedPath)	#find target city
			self.twoOptAgentState = goToCity
			predictedPath.append(goToCity)			#add target city in visited[]

		print(predictedPath)
		finalCost = self.findCostOfTravel(predictedPath)
		#print("total cost ",finalCost)

		bestCost = finalCost									#Find best cost
		bestRoute = predictedPath.copy()						#store best route

		for i in range(0 , 8):
			route1 , route2 = self.swapper(predictedPath , i , i+3)

			#print("route 1 is",route1)
			#print("route 2 is",route2)

			cost1 = self.findCostOfTravel(route1)
			cost2 = self.findCostOfTravel(route2)

			#print("total cost of route1" , cost1)
			#print("total cost of route 2" , cost2)

			if(cost1 < cost2):
				if(cost1 < bestCost):
					bestCost = cost1
					bestRoute = route1.copy()

			elif(cost2 < cost1):
				if(cost2 < bestCost):
					bestCost = cost2
					bestRoute = route2.copy()

		#print("Best Cost is" , bestCost)
		print("Best route is" , bestRoute)

		return bestRoute
					










