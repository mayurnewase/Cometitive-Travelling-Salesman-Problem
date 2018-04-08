import csv
import random
import math

no = int(raw_input("How many :"))
name = raw_input("File name :")
#no = 5
#name = "test.csv"

arr3 = [[0 for i in range(no+3)]for y in range(no)]

for i in range(0 , no):							#city ids
	arr3[i][0] = i

for i in range(0 , no):							#X & Y co-ordinates of cities
	arr3[i][1] = random.randint(0 , 550)
	arr3[i][2] = random.randint(0 , 550)
	print(arr3[i][1] , arr3[i][2])

for x_csv_index in range(0 , no):							#cost of travel
	second_city_index = x_csv_index + 1
	for y_csv_index in range(x_csv_index + 4 , no + 3):
		#arr3[i][j] = random.randint(0 , 100)
		#arr3[j-3][i+3] = arr3[i][j]
		#Distance Formula
		#sqrt( (x2-x1)**2 + (y2-y1)**2 )
		print(x_csv_index , y_csv_index , second_city_index)
		x2 = arr3[second_city_index][1]
		x1 = arr3[x_csv_index][1]
		y2 = arr3[second_city_index][2]
		y1 = arr3[x_csv_index][2]

		cost = ((x2-x1)**2) + ((y2-y1)**2)
		
		arr3[x_csv_index][y_csv_index] = math.sqrt(cost)
		arr3[y_csv_index-3][x_csv_index+3] = arr3[x_csv_index][y_csv_index]
		second_city_index += 1

header = ["id" , "x_pos" , "y_pos"]

for i in range(0 , no):						#city names
	header.append("dist" + str(i))

with open(name, 'w') as f:
	
	writer = csv.writer(f)
	writer.writerow(header)
	writer.writerows(arr3)
    