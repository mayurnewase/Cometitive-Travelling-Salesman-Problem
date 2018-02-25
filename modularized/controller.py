from multiprocessing.connection import Client
import pandas as pd
import time
import random

from prediction_utils import nearestNeighbour , twoOpt , aggressiveNeighbour
#from twoOpt import twoOpt
#from aggressive_neighbour import aggressiveNeighbour
from random_neighbour import random
#from nearest_neighbour import nearestNeighbour
from hyperX import hyperXprediction

csv_file_path = "distanceFileTwenty.csv"
df = pd.read_csv(csv_file_path)

address = ('localhost', 6000)
conn = Client(address, authkey=b'secret password')
print("trying")
address2 = ('localhost', 7000)
conn2 = Client(address2, authkey=b'secret password')

#set policy for other agent....
otherAgentPolicyForDemo = "nn"
#For start hyperX policy will be nn.
hyperXPolicy = "nn"

moves = []

agent1_state = 0
agent2_state = 0
visited = []

def takeInfoFromEnv(agent1_state , agent2_state , visited):
	agent1_state = str(conn.recv())			#get states from environment
	agent2_state = str(conn.recv())
	visited = conn.recv()
	print("Info got from env agent1_state :" , agent1_state , "agent2_state :",agent2_state)
	return agent1_state , agent2_state , visited

def giveInfoToEnv(agent1_target , agent2_target):
	conn.send(agent1_target)
	conn2.send(agent2_target)
	

#play 3 moves
#let nn vs otherAgentPolicy

print("Trying demo run....")

twoOptFullPathCalculated = False

initializeStartStates = False			#to give starting states to hyperX to find path from start,and find possibility
start_agent_state_1 = 0
start_agent_state_2 = 0
start_visited = []

twoOptPathCounter = 1					#to maintain target index from demo to actual run
visited = []
#print("before starting visited is " , visited)

for i in range(0 , 4):

	end_agent_state1 , end_agent_state2 = agent1_state , agent2_state			#to pass 1 step prev to hyperX module
	agent1_state , agent2_state , visited = takeInfoFromEnv(agent1_state , agent2_state , visited)
	#print("visited appending " , agent1_state , " " , agent2_state)
	#visited.append(int(agent1_state))
	#visited.append(int(agent2_state))
	#print(visited)
	if(not initializeStartStates):					#these to be sent to hyperX for reconstruction
		start_agent_state_1 = agent1_state
		start_agent_state_2 = agent2_state
		start_visited = visited.copy()				
		initializeStartStates  =True

	if(not twoOptFullPathCalculated):
		to2 = twoOpt(int(agent2_state))				#Find full path of agent2 for safety......
		fullPath = to2.driver()						#So if other agent uses twoOpt,then use this.
		twoOptFullPathCalculated = True

	if(otherAgentPolicyForDemo == "nn"):
		nn1 = nearestNeighbour(int(agent1_state) , visited)
		nn2 = nearestNeighbour(int(agent2_state) , visited)
		agent1_target = nn1.driver()
		agent2_target = nn2.driver()

	elif(otherAgentPolicyForDemo == "an"):
		nn1 = nearestNeighbour(int(agent1_state) , visited)
		agent1_target = nn1.driver()
		an2 = aggressiveNeighbour(int(agent2_state) , int(agent1_state) , agent1_target , visited)
		agent2_target = an2.driver()

	elif(otherAgentPolicyForDemo == "to"):				#full path is already calculated for agent 2
		agent2_target = fullPath[twoOptPathCounter]
		twoOptPathCounter += 1
		nn1 = nearestNeighbour(int(agent1_state) , visited)
		agent1_target = nn1.driver()

	elif(otherAgentPolicyForDemo == "rn"):
		rn2 = random(int(agent2_state) , visited)
		agent2_target = rn2.driver()
		nn1 = nearestNeighbour(int(agent1_state) , visited)
		agent1_target = nn1.driver()

	print("agent1_target in demo run " , agent1_target)
	print("agent2_target in demo run " , agent2_target)
	
	if(i != 3):
		giveInfoToEnv(agent1_target , agent2_target)

	moves.append(int(agent2_state))				#store only 2nd agent's moves

	agent1_state = agent1_target
	agent2_state = agent2_target


#moves.append(agent2_state)						#adding last state
#print("after demo  visited is " , visited)
while(agent1_state != -1 or agent2_state != -1):
	#find new policy from history
	
	hyperAgent = hyperXprediction(int(start_agent_state_1) , int(start_agent_state_2) , int(end_agent_state1) , int(end_agent_state2) , start_visited , visited , moves , hyperXPolicy)
	bestPolicy = hyperAgent.findBestPolicy()
	start_agent_state_1 = end_agent_state1
	start_agent_state_2 = end_agent_state2
	start_visited = visited.copy()
	moves = []
	#got policy
	print("")
	print("")
	print("visited array is " , visited)
	print("Best policy for hyperX is " , bestPolicy)
	print("Other agent is using " , otherAgentPolicyForDemo)
	print("Now playing 3 steps using best policy...")
	print("")
	print("")
	if(bestPolicy == "nn"):		#4 possibilities(nn vs otherAgentPolicy(nn,an,rn,to))
		for i in range(0 , 4):
			end_agent_state1 , end_agent_state2 = agent1_state , agent2_state

			agent1_state , agent2_state , visited = takeInfoFromEnv(agent1_state , agent2_state , visited)
			
			if(i == 0):
				start_agent_state_1 , start_agent_state_2 = agent1_state , agent2_state
			
			if(otherAgentPolicyForDemo == "nn"):

				nn1 = nearestNeighbour(int(agent1_state) , visited)
				nn2 = nearestNeighbour(int(agent2_state) , visited)
				agent1_target = nn1.driver()
				agent2_target = nn2.driver()

			elif(otherAgentPolicyForDemo == "an"):

				nn1 = nearestNeighbour(int(agent1_state) , visited)
				agent1_target = nn1.driver()
				an2 = aggressiveNeighbour(int(agent2_state) , int(agent1_state) , agent1_target , visited)
				agent2_target = an2.driver()

			elif(otherAgentPolicyForDemo == "to"):
				agent2_target = fullPath[twoOptPathCounter]
				twoOptPathCounter += 1
				nn1 = nearestNeighbour(int(agent1_state) , visited)
				agent1_target = nn1.driver()

			elif(otherAgentPolicyForDemo == "rn"):
				rn2 = random(int(agent2_state) , visited)
				agent2_target = rn2.driver()
				nn1 = nearestNeighbour(int(agent1_state) , visited)
				agent1_target = nn1.driver()				

			print("agent1_target is ", agent1_target)
			print("agent2_target is ", agent2_target)
			
			moves.append(int(agent2_state))
			
			if(agent1_target == -1 or agent2_target == -1):
				break

			if(i != 3):
				giveInfoToEnv(agent1_target , agent2_target)

			#visited.append(agent1_target)
			#visited.append(agent2_target)
			#moves.append(int(agent2_state))				#store only 2nd agent's moves

			agent1_state = agent1_target
			agent2_state = agent2_target

	elif(bestPolicy == "an"):	#4 possibilities(an vs otherAgentPolicy(nn,an,rn,to))

		for i in range(0 , 4):

			agent1_state , agent2_state , visited = takeInfoFromEnv(agent1_state , agent2_state , visited)
			
			if(otherAgentPolicyForDemo == "nn"):

				nn2 = nearestNeighbour(int(agent2_state) , visited)
				agent2_target = nn1.driver()
				an1 = aggressiveNeighbour(int(agent1_state) , int(agent2_state) , agent2_target ,visited)
				agent1_target = an2.driver()

			elif(otherAgentPolicyForDemo == "to"):
				agent2_target = fullPath[twoOptPathCounter]
				twoOptPathCounter += 1
				an1 = aggressiveNeighbour(int(agent1_state) , int(agent2_state) , agent2_target ,visited)
				agent1_target = an2.driver()				


			elif(otherAgentPolicyForDemo == "rn"):
				rn2 = random(int(agent2_state) , visited)
				agent2_target = rn2.driver()
				an1 = aggressiveNeighbour(int(agent1_state) , int(agent2_state) , agent2_target ,visited)
				agent1_target = an2.driver()

			print("agent1_target is ", agent1_target)
			print("agent2_target is ", agent2_target)
			if(agent1_target == -1 or agent2_target == -1):
				break

			giveInfoToEnv(agent1_target , agent2_target)
			
			visited.append(agent1_target)
			visited.append(agent2_target)
			moves.append(agent2_state)				#store only 2nd agent's moves

			agent1_state = agent1_target
			agent2_state = agent2_target

##------------------------------------TESTING REMAINING-------------------------------------

	elif(bestPolicy == "to"):				

		nn1 = twoOpt(int(agent1_state))
		agent1_path = nn1.driver()
		twoOptPathCounter_2 = 1

		for i in range(0 , 3):
			agent1_state , agent2_state , visited = takeInfoFromEnv(agent1_state , agent2_state , visited)

			if(otherAgentPolicyForDemo == "nn"):
	
				agent1_target = agent1_path[twoOptPathCounter_2]
				twoOptPathCounter_2 += 1
				nn2 = nearest_neighbour(int(agent2_state) , visited)
				agent2_target = nn2.driver()
			
			elif(otherAgentPolicyForDemo == "an"):

				agent1_target = agent1_path[twoOptPathCounter_2]
				twoOptPathCounter_2 += 1
				an2 = aggressiveNeighbour(int(agent2_state) , int(agent1_state) , agent1_target ,visited)
				agent2_target = an2.driver()

			elif(otherAgentPolicyForDemo == "to"):

				agent1_target = agent1_path[twoOptPathCounter_2]
				twoOptPathCounter_2 += 1

				agent2_target = fullPath[twoOptPathCounter]
				twoOptPathCounter += 1

			elif(otherAgentPolicyForDemo == "rn"):
				agent1_target = agent1_path[twoOptPathCounter_2]
				twoOptPathCounter_2 += 1

				rn2 = random(int(agent2_state) , visited)
				agent2_target = rn2.driver()


			print("agent1_target is ", agent1_target)
			print("agent2_target is ", agent2_target)
			if(agent1_target == -1 or agent2_target == -1):
				break

			giveInfoToEnv(agent1_target , agent2_target)

			visited.append(agent1_target)
			visited.append(agent2_target)
			moves.append(agent2_state)				#store only 2nd agent's moves

			agent2_state = agent2_target

	elif(bestPolicy == "rn"):

		for i in range(0 , 3):
			agent1_state , agent2_state , visited = takeInfoFromEnv(agent1_state , agent2_state , visited)

			if(otherAgentPolicyForDemo == "nn"):
				rn1 = random(int(agent1_state) , visited)
				nn2 = nearestNeighbour(int(agent2_state) , visited)
				agent1_target = nn1.driver()
				agent2_target = nn2.driver()
			
			elif(otherAgentPolicyForDemo == "an"):
				rn1 = random(int(agent1_state) , visited)
				agent1_target = rn1.driver()
				an2 = aggressiveNeighbour(int(agent2_state) , int(agent1_state) , int(agent1_target) , visited)
				agent2_target = an2.driver()

			elif(otherAgentPolicyForDemo == "to"):
				agent2_target = fullPath[twoOptPathCounter]
				twoOptPathCounter += 1
				rn1 = random(int(agent1_state) , visited)
				agent1_target = rn1.driver()

			elif(otherAgentPolicyForDemo == "rn"):
				rn1 = random(int(agent1_state) , visited)
				agent1_target = rn1.driver()
				rn2 = random(int(agent2_state) , visited)
				agent2_target = rn2.driver()				

			giveInfoToEnv(agent1_target , agent2_target)

			visited.append(agent1_target)
			visited.append(agent2_target)
			moves.append(agent2_state)				#store only 2nd agent's moves

			agent1_state = agent1_target
			agent2_state = agent2_target

	#end_agent_state1 = agent1_state
	#end_agent_state2 = agent2_state

print(visited)
conn.close()
conn2.close()












