from os import environ

from .base_maze import GenerationAlgorithm, Maze, MazeNode, SolvingAlgorithm
from .graphics import GraphicsApp

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
