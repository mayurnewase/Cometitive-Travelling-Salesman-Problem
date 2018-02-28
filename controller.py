from nearest_neighbour import nearestNeighbour
from aggressive_neighbour import aggressiveNeighbour
from multiprocessing.connection import Client
from twoOpt import twoOpt

address1 = ('localhost', 6000)
conn = Client(address1, authkey=b'secret password')

address2 = ('localhost', 7000)
conn2 = Client(address2, authkey=b'secret password')

findPath = False


while(True):

	agent1_state = str(conn.recv())
	agent2_state = str(conn.recv())
	visited = conn.recv()
	agent1_state = str(conn2.recv())
	agent2_state = str(conn2.recv())
	visited = conn2.recv()
	print("visited is ",visited)
	
	if(not findPath):
		path1 = twoOpt(int(agent1_state))
		path2 = twoOpt(int(agent2_state))
		path1 = path1.driver()
		path2 = path2.driver()
		findPath = True
		index = 0
		print("path 1 is ",path1)
		print("path 2 is ",path2)

	policy = "annn"

	if(policy == "nnan"):

		nn1 = nearestNeighbour(int(agent1_state) , visited)
		agent1_target = nn1.driver()
		an1 = aggressiveNeighbour(int(agent2_state) , int(agent1_state) , int(agent1_target) , visited)
		agent2_target = an1.driver()

	elif(policy == "nnto"):
		index += 1
		agent1_target = path1[index]
		agent2_target = path2[index]

	elif(policy == "annn"):
		print("an vs nn")
		nn2 = nearestNeighbour(int(agent2_state) , visited)
		agent2_target = nn2.driver()
		an1 = aggressiveNeighbour(int(agent1_state) , int(agent2_state) , int(agent2_target) , visited)
		agent1_target = an1.driver()		

	elif(policy == "nnnn"):
		nn1 = nearestNeighbour(int(agent1_state) , visited)
		agent1_target = nn1.driver()
		nn2 = nearestNeighbour(int(agent2_state) , visited)
		agent2_target = nn2.driver()


	conn.send(int(agent1_target))
	conn2.send(int(agent2_target))

	input("")













