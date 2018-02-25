# Cometitive-Travelling-Salesman-Problem

This is project for solving Compititive travelling salesman problem by using hyperheuristic methods.

Changelog:-
	
	Aggressive heuristic method completed.
	HyperX tseting for nn completed successfully.

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
      
4.Hyper heuristic modules:-(inside modularized directory)
      
      prediction_utils.py -> Used for reconstruction of path for predicting heuristic used by other agent.
      controller.py -> (main controller)Used for controlling agents and communication with enviroment.
      hyperX -> Used for predicting other agent's heuristic and find best policy against it.

To Do:-
      
      Test and remove bugs for multiple predictions
      



      
For more help in tkinter for gui visit https://www.python-course.eu/tkinter_canvas.php/

For tips on pandas visit http://pythonhow.com/accessing-dataframe-columns-rows-and-cells/
