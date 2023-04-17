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
<br/>
<br/>

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
<br/>

##### Solving Algorithms
 - AStarSolver
 - DijkstraSolver
 - FloodFillSolutionCheck

AStarSolver and DijkstraSolver find the shortest path between a Maze's entrance and exit. FloodFillSolutionCheck checks to see if every node in a maze can be reached from every other node.
<br/>
<br/>

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
<br/>
<br/>

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
<br/>
<br/>

### Generating a Maze solution at runtime

aamaze allows for solutions to be generated dynamically while the GraphicsApp is running. To do this:
1. Create a maze using the workflow described in Basic use case: Create a Maze and Solution (1-4) DO NOT run "solve_maze" on the SolvingAlgorithm.
```
from aamaze import Maze
from aamaze.generation import X_GeneratingAlgorithm
from aamaze.solving import Y_SolvingAlgorithm

maze = Maze(20, 10, start_filled=True, entrance_index=0, exit_index=-1)
X_GenerationAlgorithm(maze).generate_maze()
maze_solver = Y_SolvingAlgorithm(maze)
```

2. Create a GraphicsApp object
```
from aamaze import GraphicsApp
app = GraphicsApp()
```
3. (Optional) Configure whether a solution starts to be generated as soon as "app.run()" is called (start_paused), and the speed of generation (target_steps_per_second). By default, start_paused=False, target_steps_per_second=50
```
app.configure(start_paused=True, target_steps_per_second=50)
```
4. Run the app as usual
```
app.run()
```
<br/>

#### Manipulating the solving algorithm at runtime

Controls for manipulating the solving algorithm at runtime are:
 - [SPACE] to **pause/unpause** solving algorithm generation
 - [S] to **manually run one step** of the solving algorithm
 - [R] to **reset** solving algorithm
 - [+] to **increase** target_steps_per_second (speed of solution generation)
 - [-] to **decrease** target_steps_per_second (speed of solution generation)
<br/>
<br/>

### Configuring GraphicsApp

Below are all options that can be set using the app.configure() method. Options are always set using keyword args (var_x = val_y). Multiple options can be set in the same app.configure call. Available options can be printed via accessing the ".options_list" property of a GraphicsApp object instance.
Examples:
```
# app = GraphicsApp instance


app.configure(aspect_ratio=[16, 10])
app.configure(exit_colour=[200, 32, 32], entrance_colour=[32, 200, 32])
app.configure(window_width=1600, wall_colour=[0, 0, 0], show_fps_counter=True)
```
<br/>

#### Option input types Key
 - **Colour:** Set using RGB values between 0 and 255 (inclusive). Takes 3 integers in a List, Tuple or any other object that is subscriptable.
  - e.g. [200, 200, 205], (0, 4, 8), [255, 32, 16]
 - **Pair of Numbers:** Takes 2 numbers in a List, Tuple or any other object that is subscriptable.
  - e.g. [200, 100], (16, 9), [6, 4.5] 
 - **Bool:** Takes a standard python bool.
  - e.g. True, False
 - **Positive Integer:** Takes a standard python integer that is greater than or equal to 0.
  - e.g. 0, 253, 1000000
<br/>

#### Full list of options.

 - **aspect_ratio:** Sets the aspect ratio that the GraphicsApp window will open at (e.g. [16, 9]). - **Pair of Numbers**
 - **background_colour:** Sets the background colour of the GraphicsApp window (e.g. [200, 200, 205]). - **Colour**
 - **entrance_colour:** Sets colour of Start/Entrance tile of maze. - **Colour**
 - **exit_colour:** Sets colour of End/Exit tile of maze. - **Colour**
 - **show_fps_counter:** Determines whether fps counter is displayed in the top right of the GraphicsApp window. - **Bool**
 - **show_step_counter:** Determines whether target steps per second counter is displayed in the top right of the GraphicsApp window. - **Bool**
 - **solution_colour:** Sets the colour of solution nodes - **Colour**
 - **start_paused:** Determines whether the maze tries to start generating a solution as soon as GraphicsApp window is opened - **Bool**
 - **target_fps:** Target Frames per Second of the GraphicsApp window. - **Positive Integer**
 - **target_steps_per_second:** Target number of times step() method is called on the SolvingAlgorithm - **Positive Integer**
 - **wall_colour:** Sets colour of maze walls - **Colour**
 - **window_width:** Sets the width of the GraphicsApp window - **Positive Integer**
<br/>
<br/>

END
