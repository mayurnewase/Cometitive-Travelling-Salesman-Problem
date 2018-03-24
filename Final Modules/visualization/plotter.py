import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("finalResult.csv")
score1 = df.agent1
score2 = df.agent2
heuristic = df.heuristic
#print(score1)

#numbers1 = [9,4,7,3,16,51,22,62,43,19,88,7,8,54,1,33,50]
y = np.arange(16)
#numbers2 = [11,21,31,41,51,61,71,51,61,91,81,71,80,5,5,3,50]
nn = []
hnn = []
an=[]
han=[]
to=[]
hto=[]
rn=[]
hrn=[]

for i in range(len(heuristic)):
	if (heuristic[i] == "nn"):
		nn.append(score2[i])
		hnn.append(score1[i])

	if (heuristic[i] == "an"):
		an.append(score2[i])
		han.append(score1[i])

	if (heuristic[i] == "to"):
		to.append(score2[i])
		hto.append(score1[i])

	if (heuristic[i] == "rn"):
		rn.append(score2[i])
		hrn.append(score1[i])



fig, axes = plt.subplots(nrows=2, ncols=2)
ax0, ax1, ax2, ax3 = axes.flatten()

ax0.axis([0, 17 , 0 , 15000])
ax0.bar(np.arange(len(nn)) , hnn , width=0.35,color='b')
ax0.bar(np.arange(len(nn))+0.50 , nn , width=0.35 ,color='g',align='center')
ax0.set_title("nn vs hyperX")

ax1.axis([0, 17 , 0 , 15000])
ax1.bar(np.arange(len(an)) , han , width=0.35,color='b')
ax1.bar(np.arange(len(an)) + 0.50 , an , width=0.35 ,color='g',align='center')
ax1.set_title("an vs hyperX")

ax2.axis([0, 17 , 0 , 15000])
ax2.bar(np.arange(len(to)) , hto , width=0.35,color='b')
ax2.bar(np.arange(len(to)) + 0.50 , to , width=0.35 ,color='g',align='center')
ax2.set_title("to vs hyperX")

ax3.axis([0, 17 , 0 , 15000])
ax3.bar(np.arange(len(rn)) , hrn , width=0.35,color='b')
ax3.bar(np.arange(len(rn)) + 0.50 , rn , width=0.35 ,color='g',align='center')
ax3.set_title("rn vs hyperX")



#plt.tight_layout()



plt.show()



















