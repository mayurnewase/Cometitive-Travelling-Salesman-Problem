from twoOpt import optClass
from random_neighbour import randomClass
from prediction_utils import nearestNeighbour , twoOpt , aggressiveNeighbour

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
	
	hyperState = 0
	otherState = 0
	visited = []
	moves = []
	currentPolicy = ""
	probability = [0,0,0,0]

	def __init__(self , hyperState , otherState ,visited , moves , currentPolicy):

		self.hyperState = hyperState
		self.otherState = otherState
		self.visited = visited.copy()
		self.moves = moves.copy()
		self.currentPolicy = currentPolicy

		'''
		visited = [8,9]
		thisNearestAgentState = 8
		otherNearestAgentState = 9
		twoOptAgentState = 8
		aggressiveAgentState = 9
		currentPolicy = "an"	#Policy of this agent
		'''

	def predict(self):

		if(self.currentPolicy == "nn"):
			
			thisState_1 = self.hyperState
			thisState_2 = self.hyperState
			thisState_3 = self.hyperState
			
			otherState_1 = self.otherState
			otherState_2 = self.otherState
			otherState_3 = self.otherState
			#otherAgentState_1 = 9									#Do this properly for all vars...

			visited_1 = self.visited.copy()
			visited_2 = self.visited.copy()
			visited_3 = self.visited.copy()

			predictedMoves = []

			print("------NN vs AN------")
			for i in range(0 , 4):	# NN , AN
				#FIGHT BETWEEN 2 REAL AGENTS
				#Suppose the results are as follows

				#moves of nearest neighbour(this agent) = 8,1,4
				#moves of other agent(aggressive) = 9,2,10
				predictedMoves.append(otherState_1)
				#print("nn state is" , thisState_1)
				#print("nn visited is" , visited_1)
				nn = nearestNeighbour(thisState_1 , [0,0,0,0] , visited_1)	#this agent
				nearestAgentTarget = nn.driver()
				#print("Nearest agent target is ",nearestAgentTarget)
				
				if(nearestAgentTarget == -1):
					break
				
				#run aggressive 												#other agent maybe
				an = aggressiveNeighbour(otherState_1,thisState_1,nearestAgentTarget,[0,0,0,0],visited_1)
				aggressiveAgentTarget = an.driver()
				#print("Aggressive agent state is " , aggressiveAgentTarget)

				visited_1.append(nearestAgentTarget)
				visited_1.append(aggressiveAgentTarget)

				thisState_1 = nearestAgentTarget
				otherState_1 = aggressiveAgentTarget

				#Got result as
				#moves of nearest neighbour = 8,1,4
				#moves of aggressive = 9,2,10
			for i in range(0 , 4):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[1] += 1
			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)
								

		#------------------------------------

			#run nearest neighbour
			print("------NN vs NN------")
			predictedMoves = []
			for i in range(0 , 4):	#NN  , NN
				#FIGHT BETWEEN 2 REAL AGENTS
				#Suppose the results are as follows
				#moves of nearest neighbour(this agent) = 8,1,4,6
				#moves of other agent(nearest neighbour) = 9,2,10,5
				
				predictedMoves.append(otherState_2)
				nn = nearestNeighbour(thisState_2 , [0,0,0,0] , visited_2)
				#print("visited_2 is" , visited_2)
				#print("this agent state is" , thisState_2)
				nearestAgentTarget = nn.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget)
				
				#print("---")

				nn2 = nearestNeighbour(otherState_2 , [0,0,0,0] , visited_2)
				#print("visited_2 is" , visited_2)
				#print("other agent state is" , otherState_2)
				nearestAgentTarget_2 = nn2.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget_2)

				visited_2.append(nearestAgentTarget)
				visited_2.append(nearestAgentTarget_2)

				thisState_2 = nearestAgentTarget
				otherState_2 = nearestAgentTarget_2
				#Got result as
				#moves of nearest neighbour = 8,1,4,6
				#moves of nearest neighbour = 9,2,10,5
				
			for i in range(0 , 4):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[0] += 1

			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)
		#-------------------------
			print("----------->>>>>>>>>>")
			print("NN vs 2-opt")

			predictedMoves = []
			to = twoOpt(otherState_3)
			#print("2-opt agent state is" , otherState_3)
			twoOptFullPath = to.driver()
			#print("2-opt full path is ",twoOptFullPath)

			predictedMoves.append(twoOptFullPath[0])

			for i in range(0 , 3):

				nn = nearestNeighbour(thisState_3 , [0,0,0,0] , visited_3)
				#print("this agent state is" , thisState_3)
				nearestAgentTarget = nn.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget)

				
				twoOptAgentTarget = twoOptFullPath[i+1]
				#print("2-opt agent target is " , twoOptAgentTarget)
				#print("---")

				thisState_3 = nearestAgentTarget

				visited_3.append(twoOptAgentTarget)
				visited_3.append(thisState_3)
				#print(visited_3)

				predictedMoves.append(twoOptAgentTarget)

			for i in range(0 , 4):
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
			
			visited_1 = self.visited.copy()
			visited_2 = self.visited.copy()
			visited_3 = self.visited.copy()

			predictedMoves = []
			
			#FIGHT BETWEEN 2 REAL AGENTS
			#Suppose the results are as follows
			#moves of 2-opt(this agent) = 8,9,2,10
			#moves of other agent(aggressive) = 9,2,10,1

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
				an = aggressiveNeighbour(otherState_1,thisState_1,twoOptAgentTarget,[0,0,0,0],visited_1)
				aggressiveAgentTarget = an.driver()
				#print("Aggressive agent state is " , aggressiveAgentTarget)
				predictedMoves.append(otherState_1)
				visited_1.append(twoOptAgentTarget)
				visited_1.append(aggressiveAgentTarget)

				thisState_1 = twoOptAgentTarget
				otherState_1 = aggressiveAgentTarget
				#print(visited)
				

			for i in range(0 , 4):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[1] += 1

			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)
			print("-------------------------")
			#----------------------------------------------------------------------

			print("2-opt vs NN")
			predictedMoves = []
			for i in range(0 , 4):
				
				nn = nearestNeighbour(otherState_2 , [0,0,0,0] , visited_2)
				#print("other agent state is" , otherState_2)
				nearestAgentTarget = nn.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget)
				predictedMoves.append(otherState_2)

				otherState_2 = nearestAgentTarget
				twoOptAgentTarget = twoOptFullPath[i+1]

				visited_2.append(twoOptAgentTarget)
				visited_2.append(otherState_2)

				#print(visited_2)

				

			for i in range(0 , 4):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[0] += 1
			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)
			print("-------------------------")
			#----------------------------------------------------------------------
			
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
			
			visited_1 = self.visited.copy()
			visited_2 = self.visited.copy()
			visited_3 = self.visited.copy()

			predictedMoves = []
			
			print("AN vs NN")
			print("--------------")
			for i in range(0 , 4):
				nn = nearestNeighbour(otherState_1 , [0,0,0,0] , visited_1)
				#print("other agent state is" , otherState_1)
				predictedMoves.append(otherState_1)
				nearestAgentTarget = nn.driver()
				#print("nearest agent 1 target is " , nearestAgentTarget)

				an = aggressiveNeighbour(thisState_1,otherState_1,nearestAgentTarget,[0,0,0,0],visited_1)
				aggressiveAgentTarget = an.driver()
				#print("Aggressive agent state is " , aggressiveAgentTarget)

				otherState_1 = nearestAgentTarget
				thisState_1 = aggressiveAgentTarget

				visited_1.append(thisState_1)
				visited_1.append(otherState_1)
				#print(visited_1)

				#update probabilities
				

			for i in range(0 , 4):
				if(self.moves[i] == predictedMoves[i]):
					self.probability[0] += 1
			print("predictedMoves is" , predictedMoves)
			print("probability is" , self.probability)

			print("====================================")
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

				an = aggressiveNeighbour(thisState_2,otherState_2,otherAgentTarget,[0,0,0,0],visited_2)
				aggressiveAgentTarget = an.driver()
				#print("Aggressive agent state is " , aggressiveAgentTarget)

				thisState_2 = aggressiveAgentTarget

				visited_2.append(thisState_2)
				visited_2.append(otherAgentTarget)

				#print(visited_2)

			for i in range(0 , 4):
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



#twoOptAgent = optClass()
#randomAgent = randomClass()
#twoOptAgent.connectToEnvironment(6000)	#for actual play
#randomAgent.connectToEnvironment(7000)
#twoOptAgent.driver()
#randomAgent.driver()