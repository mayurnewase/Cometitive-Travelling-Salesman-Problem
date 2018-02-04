from hyperX import hyperXprediction

hyperState = 8
otherState = 9

#Be carefull while sending state of 2-opt.send only starting state,not any intermidiate state.

visited = [8,9]
moves = [9,2,10,1]			#important->add current state also at index 0.....
currentPolicy = "an"


hx = hyperXprediction(hyperState , otherState , visited , moves , currentPolicy)
hx.predict()























