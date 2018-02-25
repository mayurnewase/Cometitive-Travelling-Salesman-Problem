#from twoOpt import optClass
from random_neighbour import random
from prediction_utils import nearestNeighbour , twoOpt , aggressiveNeighbour
from nearest_neighbour import nearestNeighbour
from aggressive_neighbour import aggressiveNeighbour
from twoOpt import twoOpt
from random_neighbour import random
import pandas as pd
'''
This module will recieve ->

1)states of both agents
2)visited
3)actual moves of other agent (3 values)
4)current policy of hyperX from controller
'''

'''
probability map
[0,1,2,3]

0 -> NN
1 -> AN
2 -> 2-opt
3 -> random
'''
class hyperXprediction:
	csv_file_path = "distanceFileTen.csv"
	df = pd.read_csv(csv_file_path)	#read csv
	startAgentState1 = 0			#initial states to reconstruct same path for other agent's policy prediction
	startAgentState2 = 0
	hyperState = 0					#current final state->from which find further states
	otherState = 0					#current final state->from which find further state
	startVisited = []				#used to reconstruct path
	visited = []
	moves = []
	currentPolicy = ""
	probability = [0,0,0,0]

	def __init__(self ,startAgentState1 , startAgentState2 , hyperState , otherState , startVisited ,visited , moves , currentPolicy):

		self.startAgentState1 = startAgentState1
		self.startAgentState2 = startAgentState2
		self.hyperState = hyperState
		self.otherState = otherState
		self.startVisited = startVisited.copy()
		self.visited = visited.copy()
		self.moves = moves.copy()
		self.currentPolicy = currentPolicy
		print("")
		print("hyperX recieved data ....")
		print("startAgentState1 ",startAgentState1)
		print("startAgentState2 ",startAgentState2)
		print("hyperX currentPolicy " , currentPolicy) 
		print("moves " , moves)
		print("startVisited ", startVisited)
		print("visited" , visited)
		print("agent1_state" , hyperState)
		print("agent2_state" , otherState)
		'''
		visited = [8,9]
		thisNearestAgentState = 8
		otherNearestAgentState = 9
		twoOptAgentState = 8
		aggressiveAgentState = 9
		currentPolicy = "an"	#Policy of this agent
		'''

	def predictOtherAgentPolicy(self):
		#use start agent states to reconstruct path,and find other agent's policy.

		if(self.currentPolicy == "nn"):
			
			thisState_1 = self.startAgentState1
			thisState_2 = self.startAgentState1
			thisState_3 = self.startAgentState1
			
			otherState_1 = self.startAgentState2
			otherState_2 = self.startAgentState2
			otherState_3 = self.startAgentState2
	
			visited_1 = self.startVisited.copy()
			visited_2 = self.startVisited.copy()
			visited_3 = self.startVisited.copy()

			predictedMoves = []

			print("------NN vs AN------")
			movesPlayed = 0								#index to keep how many moves played,its used in comparing actualMoves && predictedValues.
			for i in range(0 , 4):	# NN , AN
				#FIGHT BETWEEN 2 REAL AGENTS
				#Suppose the results are as follows

				#moves of nearest neighbour(this agent) = 8,1,4
				#moves of other agent(aggressive) = 9,2,10
				
				predictedMoves.append(otherState_1)
				#print("nn state is" , thisState_1)
				#print("nn visited is" , visited_1)
				nn = nearestNeighbour(thisState_1 , visited_1)	#this agent
				nearestAgentTarget = nn.driver()
				#print("Nearest agent target is ",nearestAgentTarget)
				
				if(nearestAgentTarget == -1):
					break
				
				#run aggressive 												#other agent maybe
				an = aggressiveNeighbour(otherState_1,thisState_1,nearestAgentTarget,visited_1)
				aggressiveAgentTarget = an.driver()
				#print("Aggressive agent state is " , aggressiveAgentTarget)

				visited_1.append(nearestAgentTarget)
				visited_1.append(aggressiveAgentTarget)

				thisState_1 = nearestAgentTarget
				otherState_1 = aggressiveAgentTarget
				movesPlayed += 1
				print("agent1_state is ",thisState_1)
				print("agent2_state is ",otherState_1)
				#Got result as
				#moves of nearest neighbour = 8,1,4
				#moves of aggressive = 9,2,10


			print("predictedMoves is" , predictedMoves)
			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[1] += 1
			
			print("probability is" , self.probability)
								
		#------------------------------------

			#run nearest neighbour
			print("------NN vs NN------")
			movesPlayed = 0
			predictedMoves = []
			for i in range(0 , 4):	#NN  , NN
				#FIGHT BETWEEN 2 REAL AGENTS
				#Suppose the results are as follows
				#moves of nearest neighbour(this agent) = 8,1,4,6
				#moves of other agent(nearest neighbour) = 9,2,10,5
				
				predictedMoves.append(otherState_2)
				nn = nearestNeighbour(thisState_2 , visited_2)
				#print("visited_2 is" , visited_2)
				#print("this agent state is" , thisState_2)
				nearestAgentTarget = nn.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget)
				if(nearestAgentTarget == -1):
					break
				#print("---")

				nn2 = nearestNeighbour(otherState_2 , visited_2)
				#print("visited_2 is" , visited_2)
				#print("other agent state is" , otherState_2)
				nearestAgentTarget_2 = nn2.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget_2)

				visited_2.append(nearestAgentTarget)
				visited_2.append(nearestAgentTarget_2)

				thisState_2 = nearestAgentTarget
				otherState_2 = nearestAgentTarget_2
				movesPlayed += 1
				#Got result as
				#moves of nearest neighbour = 8,1,4,6
				#moves of nearest neighbour = 9,2,10,5
				
			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[0] += 1

			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)
		#-------------------------
			print("----------->>>>>>>>>>")
			print("NN vs 2-opt")

			movesPlayed = 0
			predictedMoves = []
			to = twoOpt(otherState_3)
			#print("2-opt agent state is" , otherState_3)
			twoOptFullPath = to.driver()
			#print("2-opt full path is ",twoOptFullPath)

			predictedMoves.append(twoOptFullPath[0])

			for i in range(0 , 3):

				nn = nearestNeighbour(thisState_3 , visited_3)
				#print("this agent state is" , thisState_3)
				nearestAgentTarget = nn.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget)
				if(nearestAgentTarget == -1):
					break
				
				twoOptAgentTarget = twoOptFullPath[i+1]
				#print("2-opt agent target is " , twoOptAgentTarget)
				#print("---")

				thisState_3 = nearestAgentTarget

				visited_3.append(twoOptAgentTarget)
				visited_3.append(thisState_3)
				#print(visited_3)

				predictedMoves.append(twoOptAgentTarget)
				movesPlayed += 1

			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[2] += 1
			
			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)			


#----------------------------this agent -> NN completed--------------------------------------------------------------


		elif(self.currentPolicy == "2opt"):

			thisState_1 = self.hyperState
			thisState_2 = self.hyperState
			thisState_3 = self.hyperState
			
			otherState_1 = self.otherState
			otherState_2 = self.otherState
			otherState_3 = self.otherState
			
			visited_1 = self.startVisited.copy()
			visited_2 = self.startVisited.copy()
			visited_3 = self.startVisited.copy()

			predictedMoves = []
			
			#FIGHT BETWEEN 2 REAL AGENTS
			#Suppose the results are as follows
			#moves of 2-opt(this agent) = 8,9,2,10
			#moves of other agent(aggressive) = 9,2,10,1
			movesPlayed = 0

			print("2-opt vs AN")

			to = twoOpt(thisState_1)
			twoOptFullPath = to.driver()
			print("2-opt full path is ",twoOptFullPath)
			#Got result as
			#2-opt path = [8, 9, 2, 10, 1, 4, 6, 7, 0, 3, 5]
			#aggressive agent moves = 2,10,1
			for i in range(0 , 4):
				#run aggressive 												#other agent maybe
				twoOptAgentTarget = twoOptFullPath[i+1]
				an = aggressiveNeighbour(otherState_1 , thisState_1 , twoOptAgentTarget , visited_1)
				aggressiveAgentTarget = an.driver()
				#print("Aggressive agent state is " , aggressiveAgentTarget)
				
				if(aggressiveAgentTarget == -1):
					break

				predictedMoves.append(otherState_1)
				visited_1.append(twoOptAgentTarget)
				visited_1.append(aggressiveAgentTarget)

				thisState_1 = twoOptAgentTarget
				otherState_1 = aggressiveAgentTarget
				movesPlayed += 1
				#print(visited)
				

			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[1] += 1

			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)
			print("-------------------------")
			#----------------------------------------------------------------------
			movesPlayed = 0

			print("2-opt vs NN")
			predictedMoves = []
			for i in range(0 , 4):
				
				nn = nearestNeighbour(otherState_2  , visited_2)
				#print("other agent state is" , otherState_2)
				nearestAgentTarget = nn.driver()
				if(nearestAgentTarget == -1):
					break
				#print("nearest agent 1 target is " , nearestAgentTarget)
				predictedMoves.append(otherState_2)

				otherState_2 = nearestAgentTarget
				twoOptAgentTarget = twoOptFullPath[i+1]

				visited_2.append(twoOptAgentTarget)
				visited_2.append(otherState_2)

				#print(visited_2)
				movesPlayed += 1
				

			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[0] += 1
			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)
			print("-------------------------")
			#----------------------------------------------------------------------
			movesPlayed = 0
			print("2-opt vs 2-opt")
			predictedMoves = []

			to_2 = twoOpt(otherState_3)
			twoOptFullPath_2 = to_2.driver()
			print("2-opt full path is ",twoOptFullPath_2)

			for i in range(0 , 4):
				visited_3.append(twoOptFullPath[i+1])
				visited_3.append(twoOptFullPath_2[i+1])
				#print(visited_3)

				predictedMoves.append(twoOptFullPath_2[i])

			for i in range(0 , 4):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[2] += 1

			

		#----------------------------this agent -> 2-opt completed--------------------------------------------------------------

		#Aggressive neighbour -> this agent

		elif(self.currentPolicy == "an"):

			thisState_1 = self.hyperState
			thisState_2 = self.hyperState
			thisState_3 = self.hyperState
			
			otherState_1 = self.otherState
			otherState_2 = self.otherState
			otherState_3 = self.otherState
			
			visited_1 = self.startVisited.copy()
			visited_2 = self.startVisited.copy()
			visited_3 = self.startVisited.copy()

			predictedMoves = []
			
			movesPlayed = 0
			print("AN vs NN")
			print("--------------")
			for i in range(0 , 4):
				nn = nearestNeighbour(otherState_1 , visited_1)
				#print("other agent state is" , otherState_1)
				predictedMoves.append(otherState_1)
				nearestAgentTarget = nn.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget)
				if(nearestAgentTarget == -1):
					break

				an = aggressiveNeighbour(thisState_1,otherState_1,nearestAgentTarget,visited_1)
				aggressiveAgentTarget = an.driver()
				#print("Aggressive agent state is " , aggressiveAgentTarget)
				if(aggressiveAgentTarget == -1):
					break

				otherState_1 = nearestAgentTarget
				thisState_1 = aggressiveAgentTarget

				visited_1.append(thisState_1)
				visited_1.append(otherState_1)
				#print(visited_1)
				movesPlayed += 1
				#update probabilities
				

			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[0] += 1
			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)

			print("====================================")
			movesPlayed = 0
			print("AN vs 2-opt")
			print("-------------")
			predictedMoves = []

			to = twoOpt(otherState_2)
			twoOptFullPath = to.driver()
			print("2-opt full path is ",twoOptFullPath)

			for i in range(0 , 4):

				predictedMoves.append(twoOptFullPath[i])
				otherState_2 = twoOptFullPath[i]
				otherAgentTarget = twoOptFullPath[i+1]

				an = aggressiveNeighbour(thisState_2,otherState_2,otherAgentTarget,visited_2)
				aggressiveAgentTarget = an.driver()

				if(aggressiveAgentTarget == -1):
					break
				#print("Aggressive agent state is " , aggressiveAgentTarget)

				thisState_2 = aggressiveAgentTarget

				visited_2.append(thisState_2)
				visited_2.append(otherAgentTarget)

				#print(visited_2)

			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[2] += 1
			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)			

			'''
			print("====================================")
			print("AN vs AN")
			print("-------------")
			#9
			an = aggressiveNeighbour(thisAggressiveAgentState_1,otherAgentState_1,nearestAgentTarget,[0,0,0,0],visited_1)
			aggressiveAgentTarget = an.driver()
			print("Aggressive agent state is " , aggressiveAgentTarget)

			#8
			an = aggressiveNeighbour(thisAggressiveAgentState_1,otherAgentState_1,nearestAgentTarget,[0,0,0,0],visited_1)
			aggressiveAgentTarget = an.driver()
			print("Aggressive agent state is " , aggressiveAgentTarget)

			# ITS DEADLOCK......
						
			'''

	def findBenifit(self , prev1_state , prev2_state , agent1_state , agent2_state , visited):#REMAINING ..GIVE IT PREV STATES ALSO..

		benifit = [0] * 2
		if(agent1_state != agent2_state):
			if(agent1_state not in visited):
				benifit[0] += 10
			if(agent2_state not in visited):
				benifit[1] += 10

		else:
			df2 = self.df.loc[prev1_state , "dist0":"dist10"]
			cost1 = df2[agent1_state]
			#print("Agent 1 transition cost " , cost1)

			df2 = self.df.loc[prev2_state , "dist0":"dist10"]
			cost2 = df2[agent2_state]
			#print("Agent 2 transition cost " , cost2)

			if(cost1 < cost2):
				benifit[0] += 10
			elif(cost1 > cost2):
				benifit[1] += 10
			elif(cost1 == cost2):	#sharing benifit
				benifit[0] += 5
				benifit[1] += 5

		return benifit[0]

	def findBestPolicy(self):

		print("\n\n")
		print("INSIDE FIND-BEST-POLICY")
		
		self.predictOtherAgentPolicy()
		print("\n")
		print("probability vector is " , self.probability)

		
		#find his policy from probability
		
		policyIndex = self.probability.index(max(self.probability))
		
		if(policyIndex == 0):
			otherPolicy = "nn"
		elif(policyIndex == 1):
			otherPolicy = "an"
		elif(policyIndex == 2):
			otherPolicy = "to"
		elif(policyIndex == 3):
			otherPolicy = "rn"

		print("predicted other agent policy is" , otherPolicy)
		#find benifit from current state till end
		print("Trying all heuristic vs ",otherPolicy)
		print("\n\n")

		allBenifits = [0] * 4
		
		if(otherPolicy == "nn"):
			#nn vs nn
			print("Trying nn vs nn")
			agent1_state = self.hyperState
			agent2_state = self.otherState
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			visited = self.visited.copy()

			unvisited = []
			for i in range(0 , 11):
				if i not in self.visited:
					unvisited.append(i)
			
			print("unvisited is ",unvisited)

			while(len(unvisited) != 0):
		
				nn1 = nearestNeighbour(agent1_state , visited)
				nn2 = nearestNeighbour(agent2_state , visited)

				hyperTarget = nn1.driver()
				otherTarget = nn2.driver()

				allBenifits[0] += self.findBenifit(agent1_state , agent2_state , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []
				for i in range(0 , 11):
					if i not in visited:
						unvisited.append(i)				
			
			print("Benifit for nn vs nn is " , allBenifits[0])
			
			#try an vs nn and find benifits
			print("\ntrying an vs nn")
			agent1_state = self.hyperState
			agent2_state = self.otherState
			visited = self.visited.copy()

			unvisited = []
			for i in range(0 , 11):
				if i not in self.visited:
					unvisited.append(i)
			
			print("unvisited is ",unvisited)
			
			while(len(unvisited) != 0):
		
				nn2 = nearestNeighbour(agent2_state , visited)
				otherTarget = nn2.driver()

				an1 = aggressiveNeighbour(agent1_state , agent2_state , otherTarget , visited)
				hyperTarget = an1.driver()
				

				allBenifits[1] += self.findBenifit(agent1_state , agent2_state , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []
				for i in range(0 , 11):
					if i not in visited:
						unvisited.append(i)

			print("Benifit for an vs nn is " , allBenifits[1])

			print("\ntrying 2-opt vs nn")
			agent1_state = self.startAgentState1
			agent2_state = self.otherState
			visited = self.visited.copy()

			unvisited = []
			for i in range(0 , 11):
				if i not in self.visited:
					unvisited.append(i)

			print("unvisited is ",unvisited)

			to = twoOpt(int(agent1_state))
			twoOptFullPath_1 = to.driver()
			
			
			while (len(unvisited) != 0):
				
				hyperTarget = twoOptFullPath_1[int(len(visited) / 2)]#How to find current index in full path
				
				nn2 = nearestNeighbour(agent2_state , visited)
				otherTarget = nn2.driver()

				allBenifits[2] += self.findBenifit(twoOptFullPath_1[(int(len(visited) / 2) - 1)] , agent2_state , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []
				for i in range(0 , 11):
					if i not in visited:
						unvisited.append(i)

			print("Benifit for 2-opt vs nn is " , allBenifits[2])
#---------------------------------------

		elif(otherPolicy == "an"):

			print("\ntrying nn vs an")
			agent1_state = self.hyperState
			agent2_state = self.otherState
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			visited = self.visited.copy()
			print("unvisited is ",unvisited)

			unvisited = []
			for i in range(0 , 11):
				if i not in self.visited:
					unvisited.append(i)

			while(len(unvisited) != 0):
		
				nn1 = nearestNeighbour(int(agent1_state) , visited)
				hyperTarget = nn1.driver()

				an2 = aggressiveNeighbour(int(agent2_state) , int(agent1_state) , int(hyperTarget) ,visited)
				otherTarget = an2.driver()

				allBenifits[0] += findBenifit(agent1_state , agent2_state , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []
				for i in range(0 , 11):
					if i not in self.visited:
						unvisited.append(i)

			print("Benifit for nn vs an is " , allBenifits[0])


			print("\ntrying 2-opt vs an")
			agent1_state = self.startAgentState1
			agent2_state = self.otherState
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			visited = self.visited.copy()
			print("unvisited is ",unvisited)

			unvisited = []
			for i in range(0 , 11):
				if i not in self.visited:
					unvisited.append(i)

			to = twoOpt(int(agent1_state) , visited)
			twoOptFullPath_1 = to.driver()

			while(len(unvisited) != 0):

				hyperTarget = twoOptFullPath_1[len(visited) / 2]#How to find current index in full path
		
				an2 = aggressiveNeighbour(int(agent2_state) , twoOptFullPath_1[(len(visited) / 2) - 1] , int(hyperTarget) ,visited)
				otherTarget = an2.driver()

				allBenifits[2] += findBenifit(twoOptFullPath_1[(len(visited) / 2) - 1] , agent2_state , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []
				for i in range(0 , 11):
					if i not in self.visited:
						unvisited.append(i)

			print("Benifit for 2-opt vs an is " , allBenifits[2])


		elif(otherPolicy == "to"):

			#nn vs to , an vs to , to vs to , rn vs to
			#find benifit vector

			print("\ntrying nn vs to")
			agent1_state = self.hyperState
			agent2_state = self.startAgentState2
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			visited = self.visited.copy()
			print("unvisited is ",unvisited)

			unvisited = []
			for i in range(0 , 11):
				if i not in self.visited:
					unvisited.append(i)


			to2 = twoOpt(int(agent2_state) , visited)
			twoOptFullPath_2 = to2.driver()
			j = 0

			while(len(unvisited) != 0):

				nn1 = nearestNeighbour(int(agent1_state) , visited)
				hyperTarget = nn1.driver()

				otherTarget = twoOptFullPath_2[len(visited) / 2]

				allBenifits[0] += findBenifit(agent1_state , twoOptFullPath_2[(len(visited) / 2) - 1] , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []

				for i in range(0 , 11):
					if i not in self.visited:
						unvisited.append(i)


			print("\ntrying an vs to")
			agent1_state = self.hyperState
			agent2_state = self.startAgentState2
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			visited = self.visited.copy()
			print("unvisited is ",unvisited)

			unvisited = []
			for i in range(0 , 11):
				if i not in self.visited:
					unvisited.append(i)


			to2 = twoOpt(int(agent2_state) , visited)
			twoOptFullPath_2 = to2.driver()
			

			while(len(unvisited) != 0):

				otherTarget = twoOptFullPath_2[len(visited) / 2]

				an1 = nearestNeighbour(int(agent1_state) , int(agent2_state) , int(otherTarget) , visited)
				hyperTarget = an1.driver()

				allBenifits[1] += findBenifit(agent1_state , twoOptFullPath_2[(len(visited) / 2) - 1] , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []

				for i in range(0 , 11):
					if i not in self.visited:
						unvisited.append(i)


			print("\ntrying to vs to")
			agent1_state = self.startAgentState1
			agent2_state = self.startAgentState2
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			visited = self.visited.copy()
			print("unvisited is ",unvisited)

			unvisited = []
			for i in range(0 , 11):
				if i not in self.visited:
					unvisited.append(i)

			to1 = twoOpt(int(agent1_state) , visited)
			twoOptFullPath_1 = to1.driver()			

			to2 = twoOpt(int(agent2_state) , visited)
			twoOptFullPath_2 = to2.driver()
			
			while(len(unvisited) != 0):

				otherTarget = twoOptFullPath_2[len(visited) / 2]
				hyperTarget = twoOptFullPath_1[len(visited) / 2]

				#carefull in finding benifit.
				#it should be (prev state) -> (current state).
				#here agent_state1 , agent_state2 are starting of path,cant be used here.
				allBenifits[2] += findBenifit(twoOptFullPath_1[(len(visited)/2) - 1] , twoOptFullPath_2[len(visited)/2 - 1] , hyperTarget , otherTarget , visited)
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []

				for i in range(0 , 11):
					if i not in self.visited:
						unvisited.append(i)
















		print("OUTSIDE FIND-BEST-POLICY")

		print("benifit vector is ",allBenifits)

		#Return best policy by max benifit....
		
		policyIndex = allBenifits.index(max(allBenifits))

		if(policyIndex == 0):
			otherPolicy = "nn"
		elif(policyIndex == 1):
			otherPolicy = "an"
		elif(policyIndex == 2):
			otherPolicy = "to"
		elif(policyIndex == 3):
			otherPolicy = "rn"


		return otherPolicy












