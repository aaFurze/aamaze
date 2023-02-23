from __future__ import annotations

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
        return {
        "top": bool(self.walls & TOP_WALL),
        "bottom": bool(self.walls & BOTTOM_WALL),
        "left": bool(self.walls & LEFT_WALL),
        "right": bool(self.walls & RIGHT_WALL)
        }
    
    def __repr__(self) -> str:
        return f"MazeNode(x={self.x}, y={self.y}, walls={self.walls})"



class GenerationAlgorithm(ABC):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    @abstractmethod
    def generate_maze(self) -> Maze:
        ...


    @staticmethod
    def add_walls(current_node: MazeNode, neighbour_node: MazeNode):
        if neighbour_node.x > current_node.x:
            neighbour_node.walls |= 0b00000010
            current_node.walls |= 0b00000001
            return
        
        if neighbour_node.x < current_node.x:
            neighbour_node.walls |= 0b00000001
            current_node.walls |= 0b00000010
            return
        
        if neighbour_node.y > current_node.y:
            neighbour_node.walls |= 0b00001011
            current_node.walls |= 0b00000111
            return
        if neighbour_node.y < current_node.y:
            neighbour_node.walls |= 0b00001000
            current_node.walls |= 0b00000100
            return

    @staticmethod
    def remove_walls(current_node: MazeNode, neighbour_node: MazeNode):
        if neighbour_node.x > current_node.x:
            neighbour_node.walls &= 0b00001101
            current_node.walls &= 0b00001110
            return
        
        if neighbour_node.x < current_node.x:
            neighbour_node.walls &= 0b00001110
            current_node.walls &= 0b00001101
            return
        
        if neighbour_node.y > current_node.y:
            neighbour_node.walls &= 0b00001011
            current_node.walls &= 0b00000111
            return
        if neighbour_node.y < current_node.y:
            neighbour_node.walls &= 0b00000111
            current_node.walls &= 0b00001011
            return



class SolvingAlgorithm(ABC):
    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze
        self.solved: bool = False
        self.solution: List[MazeNode]

        self.step_counter: int = 0
    
    @abstractmethod
    def setup_data_structures(self):
        ...

    @abstractmethod
    def solve_maze(self) -> List[MazeNode]:
        ...
    
    @abstractmethod
    def step(self):
        ...

    @abstractmethod
    def _set_solved(self) -> bool:
        ...



class Maze():

    def __init__(self, w: int, h: int) -> None:
        # (0, 0) is the bottom left of any maze.
        self.w = w
        self.h = h
        self.maze_body: List[MazeNode] = self.generate_blank_maze(self.w, self.h)

        self._index = 0


    @property
    def size(self) -> int:
        return self.w * self.h

    def check_nodes_seperated_by_wall(self, node_1: MazeNode, node_2: MazeNode) -> bool:
        if node_1.y == node_2.y - 1 and node_1.walls & TOP_WALL: return True
        if node_1.y == node_2.y + 1 and node_1.walls & BOTTOM_WALL: return True
        if node_1.x == node_2.x + 1 and node_1.walls & LEFT_WALL: return True
        if node_1.x == node_2.x - 1 and node_1.walls & RIGHT_WALL: return True
        return False
    

    def generate_blank_maze(self, width: int, height: int) -> List[MazeNode]:
        output = []

        for i in range(width * height):
            output.append(MazeNode(i % width, i // width, 0b00001111))
        
        return output
    
    @classmethod
    def get_generated_maze(cls, maze: Maze,
     generation_algorithm: GenerationAlgorithm) -> Maze:
        return generation_algorithm.generate_maze(maze)


    def get_neighbours_from_coordinates(self, x, y) -> List[MazeNode]:
        output = [self._get_node_neighbour_above(x, y), self._get_node_neighbour_below(x, y), 
        self._get_node_neighbour_left(x, y), self._get_node_neighbour_right(x, y)]

        return [value for value in output if value is not None]

    def get_node_from_coordinates(self, x: int, y: int) -> Union[MazeNode, None]:
        if x < 0 or x >= self.w: return None
        if y < 0 or y >= self.h: return None

        return self.maze_body[(y * self.w) + x]

    def get_node_index(self, node: MazeNode):
        return node.x + (node.y * self.w)

    def get_node_neighbours(self, node: MazeNode) -> List[MazeNode]:
        return self.get_neighbours_from_coordinates(node.x, node.y)


    def _get_node_neighbour_above(self, x, y) -> Union[MazeNode, None]:
        if -1 < y < self.h - 1:
            return self.maze_body[((y + 1) * self.w) + x]
    
    def _get_node_neighbour_below(self, x, y) -> Union[MazeNode, None]:
        if self.h >= y > 0: 
            return self.maze_body[((y - 1) * self.w) + x]
    
    def _get_node_neighbour_left(self, x, y) -> Union[MazeNode, None]:
        if self.w >= x > 0:
            return self.maze_body[(y * self.w) + x - 1]

    def _get_node_neighbour_right(self, x, y) -> Union[MazeNode, None]:
        if -1 < x < self.w - 1:
            return self.maze_body[(y * self.w) + x + 1]
    

    def __getitem__(self, index):
        return self.maze_body[index]

    def __iter__(self):
        return iter(self.maze_body)
    
    def __next__(self):
        if self._index < len(self.maze_body):
            output = self.maze_body[self._index]
            self._index += 1
            return output
        raise StopIteration
    
    def __repr__(self) -> str:
        return f"Maze(w={self.w}, h={self.h})"
    
    def __str__(self) -> str:
        return f"Maze({self.w}x{self.h})"
    