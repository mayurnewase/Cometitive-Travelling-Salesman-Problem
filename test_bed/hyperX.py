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
Probability map
[1,2,3,4]

1 -> NN
2 -> AN
3 -> 2-opt
4 -> random
'''
class hyperXprediction:
	
	hyperState = 0
	visited = []
	moves = []
	currentPolicy = ""

	def __init__(hyperState , visited , moves , currentPolicy):

		self.hyperState = hyperState
		self.vi








visited = [8,9]
thisNearestAgentState = 8
otherNearestAgentState = 9
twoOptAgentState = 8
aggressiveAgentState = 9


currentPolicy = "an"	#Policy of this agent

if(currentPolicy == "nn"):
	
	thisNearestAgentState_1 = thisNearestAgentState
	thisNearestAgentState_2 = thisNearestAgentState
	thisNearestAgentState_3 = thisNearestAgentState
	
	otherAgentState_1 = 9									#Do this properly for all vars...

	visited_1 = visited.copy()
	visited_2 = visited.copy()
	visited_3 = visited.copy()

	print("------NN vs AN------")
	for i in range(0 , 3):	# NN , AN
		#FIGHT BETWEEN 2 REAL AGENTS
		#Suppose the results are as follows

		#moves of nearest neighbour(this agent) = 8,1,4
		#moves of other agent(aggressive) = 9,2,10

		nn = nearestNeighbour(thisNearestAgentState_1 , [0,0,0,0] , visited_1)	#this agent
		nearestAgentTarget = nn.driver()
		print("Nearest agent target is ",nearestAgentTarget)

		#run aggressive 												#other agent maybe
		an = aggressiveNeighbour(aggressiveAgentState,thisNearestAgentState_1,nearestAgentTarget,[0,0,0,0],visited_1)
		aggressiveAgentTarget = an.driver()
		print("Aggressive agent state is " , aggressiveAgentTarget)

		visited_1.append(nearestAgentTarget)
		visited_1.append(aggressiveAgentTarget)

		thisNearestAgentState_1 = nearestAgentTarget
		aggressiveAgentState = aggressiveAgentTarget

		#Got result as
		#moves of nearest neighbour = 8,1,4
		#moves of aggressive = 9,2,10

		

#------------------------------------

	#run nearest neighbour
	print("------NN vs NN------")
	for i in range(0 , 3):	#NN  , NN
		#FIGHT BETWEEN 2 REAL AGENTS
		#Suppose the results are as follows
		#moves of nearest neighbour(this agent) = 8,1,4,6
		#moves of other agent(nearest neighbour) = 9,2,10,5
		nn = nearestNeighbour(thisNearestAgentState_2 , [0,0,0,0] , visited_2)
		print("visited_2 is" , visited_2)
		print("this agent state is" , thisNearestAgentState_2)
		nearestAgentTarget = nn.driver()
		print("nearest agent 1 target is " , nearestAgentTarget)
		
		print("---")

		nn2 = nearestNeighbour(otherNearestAgentState , [0,0,0,0] , visited_2)
		print("visited_2 is" , visited_2)
		print("other agent state is" , otherNearestAgentState)
		nearestAgentTarget_2 = nn2.driver()
		print("nearest agent 1 target is " , nearestAgentTarget_2)

		visited_2.append(nearestAgentTarget)
		visited_2.append(nearestAgentTarget_2)

		thisNearestAgentState_2 = nearestAgentTarget
		otherNearestAgentState = nearestAgentTarget_2
		#Got result as
		#moves of nearest neighbour = 8,1,4,6
		#moves of nearest neighbour = 9,2,10,5

		#update probability for other agent being NN REMAINING
#-------------------------
	print("----------->>>>>>>>>>")
	print("NN vs 2-opt")

	to = twoOpt(otherAgentState_1)
	print("2-opt agent state is" , otherAgentState_1)
	twoOptFullPath = to.driver()
	print("2-opt full path is ",twoOptFullPath)

	for i in range(0 , 3):

		nn = nearestNeighbour(thisNearestAgentState_3 , [0,0,0,0] , visited_3)
		print("this agent state is" , thisNearestAgentState_3)
		nearestAgentTarget = nn.driver()
		print("nearest agent 1 target is " , nearestAgentTarget)

		

		twoOptAgentTarget = twoOptFullPath[i+1]
		print("2-opt agent target is " , twoOptAgentTarget)
		print("---")

		thisNearestAgentState_3 = nearestAgentTarget

		visited_3.append(twoOptAgentTarget)
		visited_3.append(thisNearestAgentState_3)
		print(visited_3)

	#update probability for other agent being 2-opt REMAINING


#----------------------------this agent -> NN completed--------------------------------------------------------------


elif(currentPolicy == "2opt"):

	thisTwoOptAgentState_1 = 8
	thisTwoOptAgentState_2 = 8
	thisTwoOptAgentState_3 = 8

	otherAgentState_1 = 9
	otherAgentState_2 = 9
	otherAgentState_3 = 9

	visited = [8,9]
	visited_1 = visited.copy()
	visited_2 = visited.copy()
	visited_3 = visited.copy()


	#FIGHT BETWEEN 2 REAL AGENTS
	#Suppose the results are as follows
	#moves of 2-opt(this agent) = 8,9,2,10
	#moves of other agent(aggressive) = 9,2,10,1

	print("2-opt vs AN")

	to = twoOpt(thisTwoOptAgentState_1)
	twoOptFullPath = to.driver()
	print("2-opt full path is ",twoOptFullPath)
	#Got result as
	#2-opt path = [8, 9, 2, 10, 1, 4, 6, 7, 0, 3, 5]
	#aggressive agent moves = 2,10,1
	for i in range(0 , 3):
		#run aggressive 												#other agent maybe
		twoOptAgentTarget = twoOptFullPath[i+1]
		an = aggressiveNeighbour(otherAgentState_1,thisTwoOptAgentState_1,twoOptAgentTarget,[0,0,0,0],visited_1)
		aggressiveAgentTarget = an.driver()
		print("Aggressive agent state is " , aggressiveAgentTarget)

		visited_1.append(twoOptAgentTarget)
		visited_1.append(aggressiveAgentTarget)

		thisTwoOptAgentState_1 = twoOptAgentTarget
		otherAgentState_1 = aggressiveAgentTarget
		#print(visited)

	print("-------------------------")
	#----------------------------------------------------------------------

	print("2-opt vs NN")

	for i in range(0 , 3):
		
		nn = nearestNeighbour(otherAgentState_2 , [0,0,0,0] , visited_2)
		print("other agent state is" , otherAgentState_2)
		nearestAgentTarget = nn.driver()
		print("nearest agent 1 target is " , nearestAgentTarget)

		otherAgentState_2 = nearestAgentTarget
		twoOptAgentTarget = twoOptFullPath[i+1]

		visited_2.append(twoOptAgentTarget)
		visited_2.append(otherAgentState_2)

		print(visited_2)

	print("-------------------------")
	#----------------------------------------------------------------------
	
	print("2-opt vs 2-opt")

	to_2 = twoOpt(otherAgentState_3)
	twoOptFullPath_2 = to_2.driver()
	print("2-opt full path is ",twoOptFullPath_2)

	for i in range(0 , 3):
		visited_3.append(twoOptFullPath[i+1])
		visited_3.append(twoOptFullPath_2[i+1])
		print(visited_3)

#----------------------------this agent -> 2-opt completed--------------------------------------------------------------

#Aggressive neighbour -> this agent
	
if(currentPolicy == "an"):

	thisAggressiveAgentState_1 = 8
	thisAggressiveAgentState_2 = 8
	thisAggressiveAgentState_3 = 8

	otherAgentState_1 = 9
	otherAgentState_2 = 9
	otherAgentState_3 = 9

	visited = [8,9]
	visited_1 = visited.copy()
	visited_2 = visited.copy()
	visited_3 = visited.copy()
	
	print("AN vs NN")
	print("--------------")
	for i in range(0 , 5):
		nn = nearestNeighbour(otherAgentState_1 , [0,0,0,0] , visited_1)
		print("other agent state is" , otherAgentState_1)
		nearestAgentTarget = nn.driver()
		print("nearest agent 1 target is " , nearestAgentTarget)

		an = aggressiveNeighbour(thisAggressiveAgentState_1,otherAgentState_1,nearestAgentTarget,[0,0,0,0],visited_1)
		aggressiveAgentTarget = an.driver()
		print("Aggressive agent state is " , aggressiveAgentTarget)

		otherAgentState_1 = nearestAgentTarget
		thisAggressiveAgentState_1 = aggressiveAgentTarget

		visited_1.append(thisAggressiveAgentState_1)
		visited_1.append(otherAgentState_1)
		print(visited_1)

		#update probabilities
	print("====================================")
	print("AN vs 2-opt")
	print("-------------")

	to = twoOpt(otherAgentState_2)
	twoOptFullPath = to.driver()
	print("2-opt full path is ",twoOptFullPath)

	for i in range(0 , 3):

		otherAgentState_2 = twoOptFullPath[i]
		otherAgentTarget = twoOptFullPath[i+1]

		an = aggressiveNeighbour(thisAggressiveAgentState_2,otherAgentState_2,otherAgentTarget,[0,0,0,0],visited_2)
		aggressiveAgentTarget = an.driver()
		print("Aggressive agent state is " , aggressiveAgentTarget)

		thisAggressiveAgentState_2 = aggressiveAgentTarget

		visited_2.append(thisAggressiveAgentState_2)
		visited_2.append(otherAgentTarget)

		print(visited_2)

		#update possibilities...........
	
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





#twoOptAgent = optClass()
#randomAgent = randomClass()
#twoOptAgent.connectToEnvironment(6000)	#for actual play
#randomAgent.connectToEnvironment(7000)
#twoOptAgent.driver()
#randomAgent.driver()