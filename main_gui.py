from tkinter import *
import csv
import pandas as pd


csv_file_path = "distanceFile.csv"
df = pd.read_csv(csv_file_path)
X_pos = df.x_pos
Y_pos = df.y_pos
id = df.id

master = Tk()
w = Canvas(master , width = 600 , height = 600)
w.pack()


def drawCircle(x , y , r = 9):
	id = w.create_oval(x-r , y-r , x+r , y+r , fill = "blue")
	return id

def drawAxis(width , height):
	w.create_line(0 , 0 , width , 0 , fill = "black" , width = 5)
	w.create_line(0 , 0 , 0 , height , fill = "black" , width = 5)

	i=0
	while(i < width):
		w.create_text(i , 7 , text = i)
		i = i + 50
	i=0
	while(i < height):
		w.create_text(13 , i , text = i)
		i = i + 50

drawAxis(600 , 600)

for i in range (11):
	drawCircle(X_pos[i] , Y_pos[i])


def drawConnectivity(city1_X , city1_Y , city2_X , city2_Y):
	w.create_line(city1_X , city1_Y , city2_X , city2_Y , width = 2 , fill = "red")


for i in id:
	j=i+1
	while (j <11):
		drawConnectivity(X_pos[i] , Y_pos[i] , X_pos[j] , Y_pos[j])
		j += 1

mainloop()
