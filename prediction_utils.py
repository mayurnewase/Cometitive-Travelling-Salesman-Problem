from random import randint
import pandas as pd

class nearestNeighbour:
	nearestNeighbourState = 0
	visited = []
	csv_file_path = "distanceFileHundred.csv"

	def __init__(self ,csv_file ,nearestNeighbourState , visited):
		self.nearestNeighbourState = nearestNeighbourState
		self.visited = visited.copy()
		self.csv_file_path = csv_file

	def findNearestNeighbour(self , currentCityId , visited):
	#find neirest unvisited city to visit
	#input->
		#currentCityId : current city of agent
		#visited : visited array
		#csv_file_path = "distanceFileHundred.csv"
		df = pd.read_csv(self.csv_file_path)
		id = df.id
		dist = df.loc[currentCityId,"dist0":"dist" + str(len(id) - 1)]			#fetch distance values for current city
		#print("distance matrix of ",currentCityId , " is \n" ,dist)
		#print("Visited array " , visited)

		toCheck = []			#this array will store all city ids except current city.so agent can visit them.This is important coz distance of city to same city is 0.so agent may select this every time causing infinite loop.
		
		
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

		minDist = 999999
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
	leaveHim = True

	visited = []
	
	csv_file_path = "distanceFileHundred.csv"
	
	def __init__(self , csv_file,aggressiveState , otherAgentState ,otherAgentTarget  , visited , leaveHim):
		self.aggressiveState = aggressiveState
		self.visited = visited.copy()
		self.otherAgentState = otherAgentState
		self.otherAgentTarget = otherAgentTarget
		self.leaveHim = leaveHim
		self.csv_file_path = csv_file
		self.df = pd.read_csv(self.csv_file_path)
		self.id = self.df.id

	def findNearestNeighbour(self , currentCityId , visited):
		
		dist = self.df.loc[currentCityId,"dist0":"dist" + str(len(self.id) - 1)]
		#print("distance matrix of ", self.state , " is \n" ,dist)
		#print("should i leave him ",self.leaveHim)

		toCheck = []
		
		for cityIndex in range(len(dist)):
			if(dist[cityIndex] != 0):			#remove current city.
				#min = dist[i]
				#cityIndex = i + 1
				toCheck.append(cityIndex)		#changed
		#print("toCheck array " , toCheck)

		unVisited = []

		if(self.leaveHim == True):
			visited.append(self.otherAgentTarget)
			#print("Leaving him alone")
		#print("in pl-an tocheck is",toCheck)
		for city in toCheck:
			if city not in visited:
				unVisited.append(city)

		#print("in pl-an unvisited is ",unVisited)
		if(len(unVisited) == 0):
			return -1
		#print("unVisited array " , unVisited)

		minDist = 999999
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
			return -1,False

		row_data = self.df.loc[int(self.aggressiveState) , "dist0":"dist" + str(len(self.id) - 1)]
		cost1 = row_data[nearestCity]

		row_data = self.df.loc[int(self.aggressiveState) , "dist0":"dist" + str(len(self.id) - 1)]
		cost2 = row_data[int(self.otherAgentTarget)]

		row_data = self.df.loc[int(self.otherAgentState) , "dist0":"dist" + str(len(self.id) - 1)]
		cost3 = row_data[int(self.otherAgentTarget)]
		
		flagDitched = False

		print("in an module nearestCity ",nearestCity," otherAgentTarget",self.otherAgentTarget)
		print("cost1 ",cost1," cost2 ",cost2 ," cost3 ",cost3 , "length of visited ",len(self.visited))

		if(self.otherAgentTarget == self.aggressiveState):				#if other dumb agent choose target same as current state of this agent,then aggressive will go to nearest city,instead of remaining in current position.
			goToCity = nearestCity
		
		elif(cost2 < cost3 and not self.leaveHim):				#Aggressive agent can reach others target early
			goToCity = self.otherAgentTarget	
			print("Ditching that nigga..... LMAO")
			flagDitched = True
		
		elif(nearestCity == self.otherAgentTarget and cost1 >= cost3 and len(self.visited)+2 <= len(self.id)):	#so nn cannot hagu this...
				print("<<<<<<<<FINDING SECOND NEAREST CITY")
				self.visited.append(nearestCity)
				goToCity = self.findNearestNeighbour(int(self.aggressiveState) , self.visited)
			
			#elif(cost2 >= cost3):							#(cost2<cost3 and leaveHim=true) || (cost2>=cost3)
		else:
			goToCity = nearestCity

		#print("in pu-an module",goToCity , flagDitched)
		return goToCity , flagDitched


class twoOpt:
	
	twoOptAgentState = 0
	visited = []
	csv_file_path = "distanceFileHundred.csv"
	
	def __init__(self ,csv_file ,twoOptAgentState , visited):
		self.twoOptAgentState = twoOptAgentState
		self.visited = visited.copy()	
		self.csv_file_path = csv_file
		self.df = pd.read_csv(self.csv_file_path)
		self.id = self.df.id
	
	def findNearestNeighbour(self , currentCityId , visited):
		
		dist = self.df.loc[currentCityId,"dist0":"dist" + str(len(self.id) - 1)]			#fetch distance values for current city
		#print("distance matrix of ",currentCityId , " is \n" ,dist)
		#print("Visited array " , visited)

		toCheck = []			#this array will store all city ids except current city.so agent can visit them.This is important coz distance of city to same city is 0.so agent may select this every time causing infinite loop.
		
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
		if(len(unVisited) == 0):
			return -1
		
		minDist = 999999
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
			row_data = self.df.loc[route[i] , "dist0" : "dist" + str(len(self.id) - 1)]
			if(row_data[route[i + 1]] == 0):					#if there is no path between cities
				return 999999
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
		goToCity = 0
		unVisited = []
		
		for city in range (0,len(self.id)):
			if city not in self.visited:
				unVisited.append(city)
		
		if(len(unVisited) == 0):
			return -1

		while (goToCity != -1):
			goToCity = self.findNearestNeighbour(self.twoOptAgentState , self.visited)	#find target city
			
			if(goToCity == -1):
				break
			
			self.twoOptAgentState = goToCity
			predictedPath.append(goToCity)			#add target city in visited[]
			self.visited.append(goToCity)

		#print("predicted path by to module is ",predictedPath)
		finalCost = self.findCostOfTravel(predictedPath)
		#print("total cost for best path is ",finalCost)

		bestCost = finalCost									#Find best cost
		bestRoute = predictedPath.copy()						#store best route

		for i in range(0 , len(predictedPath)-3):
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
		#print("Best route here is" , bestRoute)

		return bestRoute[0]
					

class random:
	
	csv_file_path = "distanceFileThirty.csv"
	
	
	thisState = 0
	visited = []

	def __init__(self ,csv_file ,thisState , visited):
		self.thisState = thisState
		self.visited = visited
		self.csv_file_path = csv_file
		self.df = pd.read_csv(self.csv_file_path)
		self.id = self.df.id

	def random_neighbour(self , currentCityId , visited):

		dist = self.df.loc[currentCityId,"dist0":"dist" + str(len(self.id) - 1)]
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









