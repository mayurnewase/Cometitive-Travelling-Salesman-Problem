from twoOpt import optClass
from random_neighbour import randomClass
from prediction_utils import nearestNeighbour , twoOpt , aggressiveNeighbour

#this module will recieve -> states of both agents , visited , current policy of hyperX from controller

visited = [8,9]
thisNearestAgentState = 8
otherNearestAgentState = 9
twoOptAgentState = 8
aggressiveAgentState = 9


currentPolicy = "nn"	#Policy of this agent

if(currentPolicy == "nn"):	
	
	thisNearestAgentState_1 = thisNearestAgentState
	thisNearestAgentState_2 = thisNearestAgentState
	thisNearestAgentState_3 = thisNearestAgentState
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

		#update probability for other agent being aggressive REMAINING

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



elif(currentPolicy == "2opt"):	#2opt , AN

	#FIGHT BETWEEN 2 REAL AGENTS
	#Suppose the results are as follows
	#moves of 2-opt(this agent) = 8,9,2,10
	#moves of other agent(aggressive) = 9,2,10,1

	to = twoOpt(twoOptAgentState)
	twoOptFullPath = to.driver()
	print("2-opt full path is ",twoOptFullPath)
	#Got result as
	#2-opt path = [8, 9, 2, 10, 1, 4, 6, 7, 0, 3, 5]
	#aggressive agent moves = 2,10,1
	for i in range(0 , 3):
		#run aggressive 												#other agent maybe
		twoOptAgentTarget = twoOptFullPath[i+1]
		an = aggressiveNeighbour(aggressiveAgentState,twoOptAgentState,twoOptAgentTarget,[0,0,0,0],visited)
		aggressiveAgentTarget = an.driver()
		print("Aggressive agent state is " , aggressiveAgentTarget)

		visited.append(twoOptAgentTarget)
		visited.append(aggressiveAgentTarget)

		twoOptAgentState =twoOptAgentTarget
		aggressiveAgentState = aggressiveAgentTarget


#What if aggressive is first agent













#twoOptAgent = optClass()
#randomAgent = randomClass()
#twoOptAgent.connectToEnvironment(6000)	#for actual play
#randomAgent.connectToEnvironment(7000)
#twoOptAgent.driver()
#randomAgent.driver()