# maze-package
A collection of maze generation and solving algorithms

![Tests](https://github.com/aaFurze/aamaze/blob/main/tests/reports/tests-badge.svg)
![Coverage](https://github.com/aaFurze/aamaze/blob/main/tests/reports/coverage-badge.svg)

<br/>
<br/>

### Pre-requisites/Requirements to use the Package

- Python version 3.7+ (Program originally written using Python 3.9 interpreter)

### Setting up the Virtual Environment
It is good practice to create a virtual environment for this project (and for any other project with non-standard-library dependencies).
See this guide for how to setup and activate a virtual environment: [Python docs](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment "Python docs")

NOTE: Ensure that you activate the environment once you have created it (See Python docs)


### Installing Dependencies (User Build)
Note: This guide assumes you are in the root project directory.

#### Poetry
If you have poetry installed on your machine, simply run poetry install.
<br/>
<br/>

#### setup.py

To install the relevant packages, select the directory that requirements.txt is in and run the following command:
```
pip install .
```
<br/>
<br/>

To check that all the packages have been installed, run the following command:
```
pip list
```
This should produce an output that contains these items
```
Package    Version
---------- -------
aamaze     latest_version
pip        20.2.3
pygame     2.3.0
setuptools 49.2.1
```

You are now ready to make Mazes!
<br/>
<br/>

# Using the Package



### Supported Algorithms
##### Generating Algorithms
 - Eller
 - GrowingTree
 - Kruskals
 - Prims
 - RecursiveBacktracker
 - _RecursiveDivisor_
 - Wilsons

All Generation algorithms (with the exception of RecursiveDivisor) require a maze with all walls filled _(start_filled=True)_

##### Solving Algorithms
 - AStarSolver
 - DijkstraSolver
 - FloodFillSolutionCheck

AStarSolver and DijkstraSolver find the shortest path between a Maze's entrance and exit. FloodFillSolutionCheck checks to see if every node in a maze can be reached from every other node.

### Basic use case: Create a Maze and Solution

Creating a Maze and Solution to a Maze can be done in the following way:

 1. Create a new Maze Object (In this case a 20x10 Maze)
```
from aamaze import Maze
maze = Maze(20, 10, start_filled=True, entrance_index=0, exit_index=-1)
```
 2. Create a new GenerationAlgorithm Object
 3. Run the "generate_maze" method on GenerationAlgorithm Object
```
from aamaze.generation import X_GeneratingAlgorithm
X_GenerationAlgorithm(maze).generate_maze()
```
 4. Create a new SolvingAlgorithm
 5. Run the "solve_maze" method on SolvingAlgorithm Object
```
from aamaze.solving import Y_SolvingAlgorithm
maze_solver = Y_SolvingAlgorithm(maze)
maze_solver.solve_maze()
```

The Objects you want to keep in this case are "maze" and "maze_solver". The GenerationAlgorithm can be safely discarded once its "generate_maze" has been run.


### Basic use case: Displaying a Maze and its solution 

To display a maze and its _solution (optional)_:
 1. Generate maze and solution Objects (as shown in _Basic use case: Create a Maze and Solution_).
 2. Create a GraphicsApp Object
```
from aamaze import GraphicsApp
app = GraphicsApp()
```
 3. Call the "run" method on the GraphicsApp Object
``` 
app.run()
```

Calling "app.run()" should open a new pygame Window that displays the Maze and its associated Solution (if a solution object is provided).

END
