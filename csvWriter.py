import csv

class logWriter:
	state1 = 0
	state2 = 0
	heuristic = ""
	score1 = 0
	score2 = 0

	def __init__(self , state1 , state2 , heuristic , score1 , score2):
		print("writing logs in csv.....")
		self.state1 = state1
		self.state2 = state2
		self.heuristic = heuristic
		self.score1 = score1
		self.score2 = score2

	def write(self):
		#header = ["state1" , "state2" , "heuristic" , "score1" , "score2"]
		values = [self.state1,self.state2,str(self.heuristic),self.score1,self.score2]


		with open('finalResult.csv', 'a') as f:
		
			writer = csv.writer(f)
			#writer.writerow(header)
			writer.writerow(values)
			




























