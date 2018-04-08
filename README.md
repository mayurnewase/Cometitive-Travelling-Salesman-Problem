# Cometitive-Travelling-Salesman-Problem

This is engineering final year's project for solving Compititive travelling salesman problem by using hyperheuristic method.

Changelog:-
	
	Aggressive heuristic method completed.
	HyperX tseting for nn completed successfully.
	Centralized controller completed.
	Dataset generator completed.

Setup:-

      install python 2.x or 3.x
      install python library "tkinter". used for developing applications in gui.
      install python library "pandas". used for managing data from csv files.

Files info:-

1.Dataset and Environment:-

      dataset.csv files -> Contain dataset
      environent.py -> Environment for 2 agents,controlled using listeners.
      datasetgenerator.py -> Generate random dataset for given number of cities.

2.Connection Demo:-
      
      client.py -> Demo file for basic client-server communication.      

3.Heuristic methods:-
      
      nearest_neighbour.py -> Logic for controlling agent using NN.
      random_neighbour.py -> Logic for controlling agent using RN.
      aggressive_neighbour.py -> Logic for controlling agent using aggressive heuristic.
      twoOpt.py -> Logic for controlling agent using 2-opt heuristic.
      

4.Hyper heuristic modules:-
      
      prediction_utils.py -> Used for reconstruction of path for predicting heuristic used by other agent.
      controller.py -> (main controller)Used for controlling agents and communication with enviroment.
      hyperX -> Used for predicting other agent's heuristic and find best policy against it.

To Do:-
      
      1)second agent use 2opt.
      2)an choose second nearest clash with leaveHim.
      4)run 100 cities for 100 times.and find avg benifit(this is used in base paper).      



For more help in tkinter for gui visit https://www.python-course.eu/tkinter_canvas.php/

For tips on pandas visit http://pythonhow.com/accessing-dataframe-columns-rows-and-cells/
