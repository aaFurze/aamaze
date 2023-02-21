from typing import List, Set

from src.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL, Maze,
                           MazeNode, SolvingAlgorithm)


class FloodFillSolutionCheck(SolvingAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)

        self.visited_nodes: Set[MazeNode] = set()
        self.unchecked_nodes: List[MazeNode] = []

        self.fill_percent: float = 0  # Value between 0 and 1 depending on how many nodes were visited in the maze.
        self.fully_filled: bool = False  # True if all nodes in the maze were visited else False
    
    def solve_maze(self) -> List[MazeNode]:
        self.unchecked_nodes.append(self.maze.get_node(0, 0))
        self.visited_nodes.add(self.unchecked_nodes[0])

        while len(self.unchecked_nodes) > 0:
            current_node = self.unchecked_nodes.pop(0)
            neighbours = self.maze.get_node_neighbours(current_node.x, current_node.y)

            for neighbour_node in neighbours:
                if {neighbour_node}.issubset(self.visited_nodes): continue
                if self.seperated_by_wall(current_node, neighbour_node): continue

                self.visited_nodes.add(neighbour_node)
                self.unchecked_nodes.append(neighbour_node)
        
        self.fill_percent = len(self.visited_nodes) / len(self.maze.maze_body)
        if len(self.visited_nodes) == len(self.maze.maze_body): self.fully_filled = True

        return list(self.visited_nodes)


    @staticmethod
    def seperated_by_wall(node_1: MazeNode, node_2: MazeNode):
        if node_2.x > node_1.x and node_1.walls & RIGHT_WALL: return True
        if node_2.x < node_1.x and node_1.walls & LEFT_WALL: return True
        if node_2.y > node_1.y and node_1.walls & TOP_WALL: return True
        if node_2.y < node_1.y and node_1.walls & BOTTOM_WALL: return True

        return False


