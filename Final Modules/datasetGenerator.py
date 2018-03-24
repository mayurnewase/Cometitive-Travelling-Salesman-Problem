import csv
import random

no = int(raw_input("How many :"))
name = raw_input("File name :")

arr3 = [[0 for i in range(no+3)]for y in range(no)]

for i in range(0 , no):							#city ids
	arr3[i][0] = i

for i in range(0 , no):							#X & Y co-ordinates of cities
	arr3[i][1] = random.randint(0 , 550)
	arr3[i][2] = random.randint(0 , 550)


for i in range(0 , no):							#cost of travel
	for j in range(i+4 , no+3):
		arr3[i][j] = random.randint(0 , 100)
		arr3[j-3][i+3] = arr3[i][j]

header = ["id" , "x_pos" , "y_pos"]

for i in range(0 , no):							#city names
	header.append("dist" + str(i))

with open(name, 'w') as f:
	
	writer = csv.writer(f)
	writer.writerow(header)
	writer.writerows(arr3)
    