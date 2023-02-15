from abc import ABC, abstractmethod
from typing import Dict, List, Union

TOP_WALL = 0b00001000
BOTTOM_WALL = 0b00000100
LEFT_WALL = 0b00000010
RIGHT_WALL = 0b00000001



class MazeNode:

    def __init__(self, x: int, y: int, walls: int) -> None:
        self.x = x
        self.y = y
        self.walls = walls      #0b00001111 == top, bottom, left and right walls
    
    def get_current_walls(self) -> Dict[str, bool]:
        output = {}
        output["top"] = bool(self.walls & TOP_WALL)
        output["bottom"] = bool(self.walls & BOTTOM_WALL)
        output["left"] = bool(self.walls & LEFT_WALL)
        output["right"] = bool(self.walls & RIGHT_WALL)

        return output



class GenerationAlgorithm(ABC):

    @classmethod
    @abstractmethod
    def generate_maze(cls, maze_body: List[MazeNode]) -> List[MazeNode]:
        ...



class SolvingAlgorithm(ABC):

    @classmethod
    @abstractmethod
    def solve_maze(cls, maze_body: List[MazeNode]) -> List[MazeNode]:
        ...



class Maze():

    def __init__(self, w: int, h: int) -> None:
        # (0, 0) is the bottom left of any maze.
        self.w = w
        self.h = h

        self.maze_body: List[MazeNode] = self.generate_blank_maze(self.w, self.h)

    
    def generate_blank_maze(self, width: int, height: int) -> List[MazeNode]:
        output = []

        for i in range(width * height):
            output.append(MazeNode(i % width, i // width, 0b00001111))
        
        return output
    
    @staticmethod
    def get_generated_maze(maze_body: List[MazeNode],
     generation_algorithm: GenerationAlgorithm) -> List[MazeNode]:
        return generation_algorithm.generate_maze(maze_body)
    
    def get_node_neighbours(self, x, y) -> List[MazeNode]:
        output = [self.get_node_neighbour_above(x, y), self.get_node_neighbour_below(x, y), 
        self.get_node_neighbour_left(x, y), self.get_node_neighbour_right(x, y)]

        return [value for value in output if value is not None]
    
    def get_node_neighbour_below(self, x, y) -> Union[MazeNode, None]:
        if self.h >= y > 0: 
            return self.maze_body[((y - 1) * self.w) + x]
    
    def get_node_neighbour_above(self, x, y) -> Union[MazeNode, None]:
        if -1 < y < self.h - 1:
            return self.maze_body[((y + 1) * self.w) + x]

    def get_node_neighbour_left(self, x, y) -> Union[MazeNode, None]:
        if self.w >= x > 0:
            return self.maze_body[(y * self.w) + x - 1]

    def get_node_neighbour_right(self, x, y) -> Union[MazeNode, None]:
        print(x - self.w + 1)
        if -1 < x < self.w - 1:
            return self.maze_body[(y * self.w) + x + 1]
