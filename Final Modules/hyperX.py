#from twoOpt import optClass
#from random_neighbour import random
from prediction_utils import nearestNeighbour , twoOpt , aggressiveNeighbour
#from nearest_neighbour import nearestNeighbour
#from aggressive_neighbour import aggressiveNeighbour
#from twoOpt import twoOpt
from random_neighbour import random
import pandas as pd
'''
This module will recieve ->

1)states(start and end) of both agents
2)visited(start and end)
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
	csv_file_path = "distanceFileThreeHundred.csv"
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
	randomCitiesChosen = []
	leaveHim = False

	def __init__(self ,startAgentState1 , startAgentState2 , hyperState , otherState , startVisited ,visited , moves , currentPolicy , leaveHim):

		self.startAgentState1 = startAgentState1
		self.startAgentState2 = startAgentState2
		self.hyperState = hyperState
		self.otherState = otherState
		self.startVisited = startVisited.copy()
		self.visited = visited.copy()
		self.moves = moves.copy()
		self.currentPolicy = currentPolicy
		self.probability = [0]*4
		self.leaveHim = leaveHim
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
			
			#otherState_3 = visited_3[1]		#for 2-opt,very first city needed.(if wanna make 2-opt smart change this)

			predictedMoves = []

			print("------NN vs AN------")
			movesPlayed = 0								#index to keep how many moves played,its used in comparing actualMoves && predictedValues.
			leaveHim = self.leaveHim

			for i in range(0 , 4):	# NN , AN
				#FIGHT BETWEEN 2 REAL AGENTS
				
				predictedMoves.append(otherState_1)
				#print("nn state is" , thisState_1)
				#print("nn visited is" , visited_1)
				nn = nearestNeighbour(thisState_1 , visited_1)	#this agent
				nearestAgentTarget = nn.driver()
				#print("Nearest agent target is ",nearestAgentTarget)
				
				movesPlayed += 1

				if(nearestAgentTarget == -1):
					break

				an = aggressiveNeighbour(otherState_1,thisState_1,nearestAgentTarget,visited_1,leaveHim)
				aggressiveAgentTarget , leaveHim = an.driver()
				#run aggressive 												#other agent maybe
				#an = aggressiveNeighbour(otherState_1,thisState_1,nearestAgentTarget,visited_1)
				#aggressiveAgentTarget = an.driver()
				#print("Aggressive agent state is " , aggressiveAgentTarget)

				visited_1.append(nearestAgentTarget)
				visited_1.append(aggressiveAgentTarget)

				thisState_1 = nearestAgentTarget
				otherState_1 = aggressiveAgentTarget

				#movesPlayed += 1
				
				print("agent1_state is ",thisState_1)
				print("agent2_state is ",otherState_1)
				

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

				predictedMoves.append(otherState_2)

				nn = nearestNeighbour(thisState_2 , visited_2)
				nearestAgentTarget = nn.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget)
				movesPlayed += 1

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
				#movesPlayed += 1
				
			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[0] += 1

			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)
			
		#-------------------------
			'''
			print("----------->>>>>>>>>>")
			print("NN vs 2-opt")

			movesPlayed = 0
			predictedMoves = []
			#to = twoOpt(otherState_3 , visited_3)
			#print("2-opt agent state is" , otherState_3)
			#twoOptFullPath = to.driver()
			#print("2-opt full path is ",twoOptFullPath)
			print("appending this to predicted moves for to ",visited_3[int(len(visited_3)) - 1])
			predictedMoves.append(visited_3[int(len(visited_3)) - 1])

			movesPlayed += 1

			for i in range(0 , 3):

				nn = nearestNeighbour(thisState_3 , visited_3)
				#print("this agent state is" , thisState_3)
				nearestAgentTarget = nn.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget)
				if(nearestAgentTarget == -1):
					break
				to = twoOpt(otherState_3 , visited_3)
				twoOptAgentTarget = to.driver()
				#print("2-opt agent target is " , twoOptAgentTarget)
				#print("---")

				thisState_3 = nearestAgentTarget
				otherState_3 = twoOptAgentTarget

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
			'''

#----------------------------this agent -> NN completed--------------------------------------------------------------


		elif(self.currentPolicy == "2opt"):

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
			leaveHim = False
			#FIGHT BETWEEN 2 REAL AGENTS
			
			print("2-opt vs AN")
			movesPlayed = 0

			for i in range(0 , 4):
				predictedMoves.append(otherState_1)
				#run aggressive 

				to = twoOpt(thisState_1 , visited_1)
				twoOptAgentTarget = to.driver()
													
				an = aggressiveNeighbour(otherState_1 , thisState_1 , twoOptAgentTarget , visited_1,leaveHim)
				aggressiveAgentTarget , leaveHim = an.driver()
				#print("Aggressive agent state is " , aggressiveAgentTarget)
				movesPlayed += 1

				if(aggressiveAgentTarget == -1):
					break

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
			
			print("2-opt vs NN")
			movesPlayed = 0
			predictedMoves = []

			for i in range(0 , 4):
				
				predictedMoves.append(otherState_2)

				nn = nearestNeighbour(otherState_2  , visited_2)
				nearestAgentTarget = nn.driver()

				to = twoOpt(thisState_2 , visited_2)
				twoOptAgentTarget = to.driver()

				movesPlayed += 1

				if(nearestAgentTarget == -1):
					break
				#print("nearest agent 1 target is " , nearestAgentTarget)
				

				otherState_2 = nearestAgentTarget
				thisState_2 = twoOptAgentTarget

				visited_2.append(twoOptAgentTarget)
				visited_2.append(otherState_2)

			
			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[0] += 1
			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)
			print("-------------------------")
			#----------------------------------------------------------------------
			
			print("2-opt vs 2-opt")
			predictedMoves = []
			movesPlayed = 0

			to_2 = twoOpt(otherState_3)
			twoOptFullPath_2 = to_2.driver()
			print("2-opt full path is ",twoOptFullPath_2)

			for i in range(0 , 4):
				to1 = twoOpt(thisState_3 , visited_3)
				twoOptAgentTarget_1 = to1.driver()

				to2 = twoOpt(otherState_3 , visited_3)
				twoOptAgentTarget_2 = to2.driver()

				visited_3.append(twoOptAgentTarget_1)
				visited_3.append(twoOptAgentTarget_2)
				
				predictedMoves.append(twoOptAgentTarget_2)

			for i in range(0 , 4):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[2] += 1

			

		#----------------------------this agent -> 2-opt completed--------------------------------------------------------------

		#Aggressive neighbour -> this agent

		elif(self.currentPolicy == "an"):

			thisState_1 = self.startAgentState1
			thisState_2 = self.startAgentState1
			thisState_3 = self.startAgentState1
			
			otherState_1 = self.startAgentState2
			otherState_2 = self.startAgentState2
			otherState_3 = self.startAgentState2
	
			visited_1 = self.startVisited.copy()
			visited_2 = self.startVisited.copy()
			visited_3 = self.startVisited.copy()

			leaveHim = False
			
			print("AN vs NN")
			predictedMoves = []
			movesPlayed = 0
			print("--------------")

			for i in range(0 , len(self.moves)):
				
				predictedMoves.append(otherState_1)

				nn = nearestNeighbour(otherState_1 , visited_1)
				#print("other agent state is" , otherState_1)
				
				nearestAgentTarget = nn.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget)
				movesPlayed += 1

				if(nearestAgentTarget == -1):
					break

				an = aggressiveNeighbour(thisState_1,otherState_1,nearestAgentTarget,visited_1,leaveHim)
				aggressiveAgentTarget , leaveHim = an.driver()
				#print("Aggressive agent state is " , aggressiveAgentTarget)
				if(aggressiveAgentTarget == -1):
					break

				otherState_1 = nearestAgentTarget
				thisState_1 = aggressiveAgentTarget

				visited_1.append(thisState_1)
				visited_1.append(otherState_1)
				#print(visited_1)
				
				#update probabilities
				

			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[0] += 1
			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)

			#--------------------------------------------
			'''
			print("AN vs 2-opt")
			print("-------------")
			movesPlayed = 0
			predictedMoves = []
			leaveHim = False

			#to = twoOpt(otherState_2)
			#twoOptFullPath = to.driver()
			#print("2-opt full path is ",twoOptFullPath)
			
			predictedMoves.append(visited_2[int(len(visited_2)) - 1])
			movesPlayed += 1

			for i in range(0 , 3):

				#predictedMoves.append(twoOptFullPath[i])
				to = twoOpt(int(otherState_2) , visited_2)
				otherAgentTarget = to.driver()

				#otherAgentTarget = twoOptFullPath[i+1]

				an = aggressiveNeighbour(thisState_2 , otherState_2 , otherAgentTarget , visited_2,leaveHim)
				aggressiveAgentTarget , leaveHim = an.driver()

				movesPlayed += 1
				
				if(aggressiveAgentTarget == -1):
					break
				#print("Aggressive agent state is " , aggressiveAgentTarget)

				thisState_2 = aggressiveAgentTarget
				otherState_2 = otherAgentTarget

				predictedMoves.append(otherAgentTarget)

				visited_2.append(thisState_2)
				visited_2.append(otherAgentTarget)

				#print(visited_2)

			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[2] += 1
			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)			
			'''
			#-----------------------------------------------------

			print("====================================")
			print("AN vs AN")
			print("-------------")
			
			movesPlayed = 0
			predictedMoves = []
			leaveHim = False
			ditchingChance = 1

			for i in range(0 , len(self.moves)):
				
				predictedMoves.append(otherState_3)
				'''
				if(ditchingChance == 1):
					an1 = aggressiveNeighbour(int(thisState_3),int(otherState_3),int(agent2_target),visited_3,False)
					agent1_target , leaveHim = an1.driver()

					if(leaveHim == True):
						ditchingChance = 2

					an2 = aggressiveNeighbour(int(otherState_3),int(thisState_3),int(agent1_target),visited_3,True)
					agent2_target , leaveHim = an2.driver()
					#ditchingChance = 2

				elif(ditchingChance == 2):
					an1 = aggressiveNeighbour(int(thisState_3),int(otherState_3),int(0),visited_3,True)		#no need of other's target
					agent1_target , leaveHim = an1.driver()
					
					an2 = aggressiveNeighbour(int(otherState_3),int(thisState_3),int(agent1_target),visited_3,False)
					agent2_target , leaveHim = an2.driver()
					
					if(leaveHim == True):
						ditchingChance = 1
				'''
				if(ditchingChance == 1):
					an2 = aggressiveNeighbour(int(otherState_3),int(thisState_3),int(0),visited_3,True)
					agent2_target , leaveHim = an2.driver()

					an1 = aggressiveNeighbour(int(thisState_3),int(otherState_3),int(agent2_target),visited_3,False)
					agent1_target , leaveHim = an1.driver()

					if(leaveHim == True):
						ditchingChance = 2
					#ditchingChance = 2

				elif(ditchingChance == 2):
					an1 = aggressiveNeighbour(int(thisState_3),int(otherState_3),int(0),visited_3,True)		#no need of other's target
					agent1_target , leaveHim = an1.driver()
					
					an2 = aggressiveNeighbour(int(otherState_3),int(thisState_3),int(agent1_target),visited_3,False)
					agent2_target , leaveHim = an2.driver()
					
					if(leaveHim == True):
						ditchingChance = 1

				movesPlayed += 1

				if(agent1_target == -1 or agent2_target == -1):
					break

				otherState_3 = agent2_target
				thisState_3 = agent1_target
				print("appending this states in an-an",otherState_3)
				#predictedMoves.append(otherState_3)

				visited_3.append(thisState_3)
				visited_3.append(otherState_3)
				#print(visited_1)
				
				#update probabilities
				

			for i in range(0 , movesPlayed):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[1] += 1
			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)


	def findBenifit(self , prev1_state , prev2_state , agent1_state , agent2_state , visited , verbose = False):

		benifit = [0] * 2
		costOfTravel = [0] * 2
		
		if(verbose == True):
			print("prev states ",prev1_state ," " ,prev2_state)
			print("target states ",agent1_state ," " ,agent2_state)
		
		if(agent1_state != agent2_state):
			if(agent1_state not in visited):
				benifit[0] += 200
			if(agent2_state not in visited):
				benifit[1] += 200

		else:
			df2 = self.df.loc[prev1_state , "dist0":"dist299"]
			cost1 = df2[agent1_state]
			#print("Agent 1 transition cost " , cost1)

			df2 = self.df.loc[prev2_state , "dist0":"dist299"]
			cost2 = df2[agent2_state]
			#print("Agent 2 transition cost " , cost2)

			if(cost1 < cost2):
				benifit[0] += 200
			elif(cost1 > cost2):
				benifit[1] += 200
			elif(cost1 == cost2):	#sharing benifit
				benifit[0] += 100
				benifit[1] += 100

		df2 = self.df.loc[prev1_state , "dist0":"dist299"]
		cost1 = df2[agent1_state]
		costOfTravel[0] += cost1

		df2 = self.df.loc[prev2_state , "dist0":"dist299"]
		cost2 = df2[agent2_state]
		costOfTravel[1] += cost2

		finalBenifit_1 = benifit[0] - costOfTravel[0]
		finalBenifit_2 = benifit[1] - costOfTravel[1]
		if(verbose == True):
			print("costs are ",cost1 , " " , cost2)
			print("benifits are ",finalBenifit_1 , " " , finalBenifit_2)
		
		return finalBenifit_1

	def findBestPolicy(self):

		print("\n\n")
		print("INSIDE FIND-BEST-POLICY")
		
		self.predictOtherAgentPolicy()
		print("------------------------")
		print("\n")
		print("probability vector is " , self.probability)
		print("\n")
		
		#find his policy from probability
		
		policyIndex = self.probability.index(max(self.probability))
		
		if(self.probability[0] < 4 and self.probability[1] < 4 and self.probability[2] < 4 and self.moves == 4):
			print("random agent detected...use an for hyperX")
			otherPolicy = "rn"

		elif(policyIndex == 0):
			otherPolicy = "nn"
		elif(policyIndex == 1):
			otherPolicy = "an"
		elif(policyIndex == 2):
			otherPolicy = "to"

		print("predicted other agent policy is" , otherPolicy)
		print("\n")
		#find benifit from current state till end
		print("Trying all heuristic vs ",otherPolicy)
		print("\n")

		allBenifits = [0] * 4
		
		if(otherPolicy == "nn"):
			#nn vs nn
			print("Trying nn vs nn")
			agent1_state = self.hyperState
			agent2_state = self.otherState
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			visited = self.visited.copy()

			unvisited = []
			for i in range(0 , 300):
				if i not in self.visited:
					unvisited.append(i)
			
			print("unvisited is ",unvisited)

			while(len(unvisited) != 0):
		
				nn1 = nearestNeighbour(agent1_state , visited)
				nn2 = nearestNeighbour(agent2_state , visited)

				hyperTarget = nn1.driver()
				otherTarget = nn2.driver()

				if(otherTarget == -1 or hyperTarget == -1):
					break

				allBenifits[0] += self.findBenifit(agent1_state , agent2_state , hyperTarget , otherTarget , visited , verbose=True)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []
				for i in range(0 , 300):
					if i not in visited:
						unvisited.append(i)				
			
			print("Benifit for nn vs nn is " , allBenifits[0])
			
			#try an vs nn and find benifits
			print("\ntrying an vs nn")
			agent1_state = self.hyperState
			agent2_state = self.otherState
			visited = self.visited.copy()
			leaveHim = False
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)

			unvisited = []
			for i in range(0 , 300):
				if i not in self.visited:
					unvisited.append(i)
			
			print("unvisited is ",unvisited)
			
			while(len(unvisited) != 0):
		
				nn2 = nearestNeighbour(agent2_state , visited)
				otherTarget = nn2.driver()

				an1 = aggressiveNeighbour(agent1_state , agent2_state , otherTarget , visited,leaveHim)
				hyperTarget , leaveHim = an1.driver()
				

				if(otherTarget == -1 or hyperTarget == -1):
					break

				allBenifits[1] += self.findBenifit(agent1_state , agent2_state , hyperTarget , otherTarget , visited , verbose = True)#benifit of nn for hyper
				#print("benifit for an is" , allBenifits[1])
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []
				for i in range(0 , 300):
					if i not in visited:
						unvisited.append(i)

			print("Benifit for an vs nn is " , allBenifits[1])
			'''
			print("\ntrying 2-opt vs nn")
			#agent1_state = self.startAgentState1
			agent1_state = self.hyperState
			agent2_state = self.otherState

			visited = self.visited.copy()

			unvisited = []
			for i in range(0 , 300):
				if i not in self.visited:
					unvisited.append(i)

			print("unvisited is ",unvisited)

			while (len(unvisited) != 0):
				
				#hyperTarget = twoOptFullPath_1[int(len(visited) / 2)]#How to find current index in full path
				to = twoOpt(int(agent1_state) , visited)
				hyperTarget = to.driver()
				
				nn2 = nearestNeighbour(int(agent2_state) , visited)
				otherTarget = nn2.driver()

				allBenifits[2] += self.findBenifit(agent1_state , agent2_state , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []
				for i in range(0 , 300):
					if i not in visited:
						unvisited.append(i)

			print("Benifit for 2-opt vs nn is " , allBenifits[2])
			#---------------------------------------
			'''

		elif(otherPolicy == "an"):

			print("\ntrying nn vs an")
			agent1_state = self.hyperState
			agent2_state = self.otherState
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			visited = self.visited.copy()
			leaveHim = False

			unvisited = []
			
			for i in range(0 , 300):
				if i not in self.visited:
					unvisited.append(i)

			print("unvisited is ",unvisited)
			while(int(agent1_state) != -1 or int(agent2_state) != -1):			#RISKY CHANGE FOR -1 INDEX ISSUE
		
				nn1 = nearestNeighbour(int(agent1_state) , visited)
				hyperTarget = nn1.driver()

				an2 = aggressiveNeighbour(int(agent2_state) , int(agent1_state) , int(hyperTarget) ,visited,leaveHim)
				otherTarget , leaveHim = an2.driver()

				if(otherTarget == -1 or hyperTarget == -1):
					break

				allBenifits[0] += self.findBenifit(agent1_state , agent2_state , hyperTarget , otherTarget , visited,verbose = True)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []
				for i in range(0 , 300):
					if i not in self.visited:
						unvisited.append(i)

			print("Benifit for nn vs an is " , allBenifits[0])

			'''
			print("\ntrying 2-opt vs an")
			#agent1_state = self.startAgentState1
			agent1_state = self.hyperState
			agent2_state = self.otherState

			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			visited = self.visited.copy()
			print("unvisited is ",unvisited)
			leaveHim = False

			unvisited = []
			for i in range(0 , 300):
				if i not in self.visited:
					unvisited.append(i)

			#to = twoOpt(int(agent1_state))
			#twoOptFullPath_1 = to.driver()

			while(agent1_state != -1 or agent2_state != -1):

				#hyperTarget = twoOptFullPath_1[int(len(visited) / 2)]#How to find current index in full path
				to = twoOpt(int(agent1_state) , visited)
				hyperTarget= to.driver()

				an2 = aggressiveNeighbour(int(agent2_state) , int(agent1_state) , int(hyperTarget) ,visited,leaveHim)
				otherTarget , leaveHim = an2.driver()
				
				if(otherTarget == -1):
					break

				allBenifits[2] += self.findBenifit(int(agent1_state) , agent2_state , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []
				for i in range(0 , 300):
					if i not in self.visited:
						unvisited.append(i)

			print("Benifit for 2-opt vs an is " , allBenifits[2])
			'''
			print("\ntrying rn vs an")
			agent1_state = self.hyperState
			agent2_state = self.otherState
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			visited = self.visited.copy()
			leaveHim = False

			for i in range(0 , 300):				#useless now..can be removed
				if i not in self.visited:
					unvisited.append(i)
			
			addRandomCityIndex = 0

			while(int(agent1_state) != -1):			#RISKY CHANGE FOR -1 INDEX ISSUE
		
				rn1 = random(int(agent1_state) , visited)
				hyperTarget = rn1.driver()
				#self.randomCitiesChosen[addRandomCityIndex] = int(hyperTarget)
				self.randomCitiesChosen.append(int(hyperTarget))
				addRandomCityIndex += 1

				if(hyperTarget == -1):
					break

				an2 = aggressiveNeighbour(int(agent2_state) , int(agent1_state) , int(hyperTarget) ,visited,leaveHim)
				otherTarget , leaveHim = an2.driver()

				if(otherTarget == -1):
					break

				allBenifits[3] += self.findBenifit(agent1_state , agent2_state , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []						#useless now..can be removed
				for i in range(0 , 300):
					if i not in self.visited:
						unvisited.append(i)

			print("Benifit for rn vs an is " , allBenifits[3])

			print("\ntrying an vs an")
			agent1_state = self.hyperState
			agent2_state = self.otherState
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			visited = self.visited.copy()
			leaveHim = False
			ditchingChance = 1

			while(int(agent1_state) != -1):

				if(ditchingChance == 1):
						print("agent2 playing")
						an2 = aggressiveNeighbour(int(agent2_state),int(agent1_state),int(0),visited,True)
						agent2_target , leaveHim = an2.driver()
						print("agent1 playing")
						an1 = aggressiveNeighbour(int(agent1_state),int(agent2_state),int(agent2_target),visited,False)
						agent1_target , leaveHim = an1.driver()

						if(leaveHim == True):
							ditchingChance = 2
							print("agent1 ditched agent2.now switching chance.")	
						#ditchingChance = 2

				elif(ditchingChance == 2):
					print("agent1 playing")
					an1 = aggressiveNeighbour(int(agent1_state),int(agent2_state),int(0),visited,True)
					agent1_target , leaveHim = an1.driver()
					
					print("agent2 playing")
					an2 = aggressiveNeighbour(int(agent2_state),int(agent1_state),int(agent1_target),visited,False)
					agent2_target , leaveHim = an2.driver()
					
					if(leaveHim == True):
						ditchingChance = 1
						print("agent2 ditched agent1.now switching chance.")

				allBenifits[1] += self.findBenifit(agent1_state , agent2_state , int(agent1_target) , int(agent2_target) , visited,verbose = True)#benifit of nn for hyper
				#print(allBenifits[1])
				agent1_state = agent1_target
				agent2_state = agent2_target

				visited.append(agent1_state)
				visited.append(agent2_state)
				#print("states are " , agent1_state , agent2_state)
			print("Benifit for an vs an is " , allBenifits[1])
		

		elif(otherPolicy == "to"):

			#nn vs to , an vs to , to vs to , rn vs to
			#find benifit vector

			print("\ntrying nn vs to")
			#agent1_state = self.hyperState

			agent1_state = self.hyperState
			visited = self.visited.copy()
			agent2_state = visited[1]				#2-opt path need very first starting position for costruction of path.(if in future you wanna make 2opt smart then change this)
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)

			unvisited = []
			for i in range(0 , 300):
				if i not in self.visited:
					unvisited.append(i)

			print("unvisited is ",unvisited)

			to2 = twoOpt(int(agent2_state))
			twoOptFullPath_2 = to2.driver()
			j = 0

			while(agent1_state != -1 or agent2_state != -1):

				nn1 = nearestNeighbour(int(agent1_state) , visited)
				hyperTarget = nn1.driver()

				if(hyperTarget == -1):
					break

				otherTarget = twoOptFullPath_2[int(len(visited) / 2)]

				print("agent1_state =", hyperTarget,"agent2_state =",otherTarget)
				allBenifits[0] += self.findBenifit(agent1_state , twoOptFullPath_2[int(len(visited) / 2) - 1] , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []

				for i in range(0 , 300):
					if i not in self.visited:
						unvisited.append(i)


			print("\ntrying an vs to")
			agent1_state = self.hyperState
			visited = self.visited.copy()
			agent2_state = visited[1]
			print("unvisited is ",unvisited)
			print("agent1_state is ",agent1_state , "agent1_state is ", agent2_state)
			leaveHim = False

			unvisited = []
			for i in range(0 , 300):
				if i not in self.visited:
					unvisited.append(i)


			to2 = twoOpt(int(agent2_state))
			twoOptFullPath_2 = to2.driver()
			

			while(agent1_state != -1 or agent2_state != -1):

				otherTarget = twoOptFullPath_2[int(len(visited) / 2)]

				an2 = aggressiveNeighbour(int(agent1_state) , int(agent2_state) , int(otherTarget) ,visited,leaveHim)
				hyperTarget , leaveHim = an2.driver()

				print("agent1_state =", hyperTarget,"agent2_state =",otherTarget)

				if(hyperTarget == -1):
					break

				allBenifits[1] += self.findBenifit(agent1_state , twoOptFullPath_2[int(len(visited) / 2) - 1] , hyperTarget , otherTarget , visited)#benifit of nn for hyper
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []

				for i in range(0 , 300):
					if i not in self.visited:
						unvisited.append(i)


			print("\ntrying to vs to")

			
			visited = self.visited.copy()
			agent1_state = visited[0]
			agent2_state = visited[1]
			
			unvisited = []
			for i in range(0 , 300):
				if i not in self.visited:
					unvisited.append(i)
			print("unvisited is ",unvisited)

			to1 = twoOpt(int(agent1_state))
			twoOptFullPath_1 = to1.driver()			

			to2 = twoOpt(int(agent2_state))
			twoOptFullPath_2 = to2.driver()
			
			while(len(unvisited) != 0):

				otherTarget = twoOptFullPath_2[int(len(visited) / 2)]
				hyperTarget = twoOptFullPath_1[int(len(visited) / 2)]

				print("agent1_state =", hyperTarget,"agent2_state =",otherTarget)
				#carefull in finding benifit.
				#it should be (prev state) -> (current state).
				#here agent_state1 , agent_state2 are starting of path,cant be used here.
				allBenifits[2] += self.findBenifit(twoOptFullPath_1[int(len(visited)/2) - 1] , twoOptFullPath_2[int(len(visited)/2 - 1)] , hyperTarget , otherTarget , visited)
				
				agent1_state = hyperTarget
				agent2_state = otherTarget

				visited.append(agent1_state)
				visited.append(agent2_state)

				unvisited = []

				for i in range(0 , 300):
					if i not in visited:
						unvisited.append(i)
				print("unvisited is",unvisited)


		elif(otherPolicy == "rn"):
			print("agent 2 is using random agent.bestPolicy for hyperX is an.")
			return "an" , 1


		print("OUTSIDE FIND-BEST-POLICY")

		print("benifit vector is ",allBenifits)

		#Return best policy by max benifit....
		
		policyIndex = allBenifits.index(max(allBenifits))

		if(allBenifits[policyIndex] == 0):
			print("\nVooillaaaa It's Done.............")
			return "its_over" , 1

		#check if benifit for an and nn are same.if yes force bestPolicy as an.
		
		if(allBenifits[policyIndex] == allBenifits[1]):
			return "an" , 1
		

		if(policyIndex == 0):
			bestHyperXPolicy = "nn"
		elif(policyIndex == 1):
			bestHyperXPolicy = "an"
		elif(policyIndex == 2):
			bestHyperXPolicy = "to"
		elif(policyIndex == 3):
			bestHyperXPolicy = "rn"
			return "rn" , randomCitiesChosen

		return bestHyperXPolicy , 1












