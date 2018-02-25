from multiprocessing.connection import Client
import pandas as pd
import time

class 2opt:
	
	csv_file_path = "distanceFile.csv"
	df = pd.read_csv(csv_file_path)
	address = ('localhost', 6000)
	conn = Client(address, authkey=b'secret password')

	thisState = 0

	def __init__(self , thisState):
		self.thisState = thisState

	def findNearestNeighbour(self , currentCityId , visited):
		#find neirest unvisited city to visit
		#input->
			#currentCityId : current city of agent
			#visited : visited array
		
		dist = df.loc[currentCityId,"dist0":"dist10"]			#fetch distance values for current city
		print("distance matrix of ",currentCityId , " is \n" ,dist)
		print("Visited array " , visited)

		toCheck = []			#this array will store all city ids except current city.so agent can visit them.This is important coz distance of city to same city is 0.so agent may select this every time causing infinite loop.
		
		min = 9999
		for cityIndex in range(len(dist)):
			if(dist[cityIndex] != 0):			#remove current and unreachable cities.
				#min = dist[i]
				#cityIndex = i + 1
				toCheck.append(cityIndex)		#changed
		print("toCheck array " , toCheck)

		unVisited = []			#this array will contain unvisited cities ids

		for city in toCheck:
			if city not in visited:
				unVisited.append(city)

		print("unVisited array " , unVisited)

		minDist = 9999
		for city in unVisited:			#now find nearest city
			if (dist[city] < minDist):
				minDist = dist[city]
				#print("city equaling to visit" , city)
				cityToVisit = city

		print("cityToVisit " , cityToVisit)
		print("====================================")
		return cityToVisit				#return target city to visit

	def findCostOfTravel(self , route):

		cost = 0
		for i in range(len(route) - 1):
			row_data = df.loc[route[i] , "dist0" : "dist10"]
			if(row_data[route[i + 1]] == 0):					#if there is no path between cities
				return 9999
			cost += row_data[route[i+1]]

		return cost

	def swapper(self , route , startCityIndex , endCityIndex):
		print("startCity is ",startCityIndex)
		print("endCity is ",endCityIndex)

		route1 = route.copy()
		route2 = route.copy()

		city0 = route[startCityIndex]
		city1 = route[startCityIndex+1]
		city2 = route[startCityIndex+2]
		city3 = route[startCityIndex+3]

		print("Cities are  ",city0 , city1 , city2 , city3)
		
		route1[startCityIndex + 1] = city2			#1 & 2
		route1[startCityIndex + 2] = city1

		route2[startCityIndex + 1] = city3			#1 & 2 & 3
		route2[startCityIndex + 2] = city1
		route2[startCityIndex + 3] = city2

		return route1 , route2

	def driver(self):

		predictedPath = []	#store visited cities
		visited = []
		initialStateAdded = False

		#print("agent1_state recieved is ",agent1_state)
		#print("agent2_state recieved is ",agent2_state)
		#print("states are ",agent1_state , agent2_state)

		#while(len(visited) < 11):		#commented to make this agent dumb(calculate full path only once)...

		initialStateAdded = False
		#agent1_state = str(conn.recv())
		agent1_state = self.thisState
		#agent2_state = str(conn.recv())
		#visited = conn.recv()
		predictedPath = []


		while (len(predictedPath) < 11):
			
			if(initialStateAdded == False):			#add initial state in visited[]
				predictedPath.append(int(agent1_state))			#AGENT NO DEPENDENT
				initialStateAdded = True

			goToCity = self.findNearestNeighbour(int(agent1_state) , predictedPath)	#AGENT NO DEPENDENT
			agent1_state = goToCity
			predictedPath.append(goToCity)			#add target city in visited[]

		print(predictedPath)
		finalCost = self.findCostOfTravel(predictedPath)
		print("total cost ",finalCost)

		bestCost = finalCost									#Find best cost
		bestRoute = predictedPath.copy()						#store best route

		for i in range(0 , 8):
			route1 , route2 = self.swapper(predictedPath , i , i+3)

			print("route 1 is",route1)
			print("route 2 is",route2)

			cost1 = self.findCostOfTravel(route1)
			cost2 = self.findCostOfTravel(route2)

			print("total cost of route1" , cost1)
			print("total cost of route 2" , cost2)

			if(cost1 < cost2):
				if(cost1 < bestCost):
					bestCost = cost1
					bestRoute = route1.copy()

			elif(cost2 < cost1):
				if(cost2 < bestCost):
					bestCost = cost2
					bestRoute = route2.copy()

		print("Best Cost is" , bestCost)
		print("Best route is" , bestRoute)

		#send first city of best route
		#for i in range(1 , len(bestRoute)):				#dont send first city again->coz it's current state and is already visited
		#	conn.send(bestRoute[i])
		#	input("")
		return bestRoute


#[8, 9, 2, 10, 1, 4, 6, 7, 0, 3, 5]


