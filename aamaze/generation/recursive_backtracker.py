import random
from typing import List

from aamaze.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL,
                              GenerationAlgorithm, Maze, MazeNode)


class RecursiveBacktracker(GenerationAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)
        self.visited_nodes: List[MazeNode] = []
    
    def generate_maze(self) -> Maze:
        if self.maze.size <= 1: return self.maze.maze_body

        # Pick a start Node
        self.visited_nodes.append(self.maze.get_node_from_coordinates(0, 0))
        node_index = 0

        while len(self.visited_nodes) < self.maze.size:


            current_neighbour_nodes = self.maze.get_neighbours_from_coordinates(self.visited_nodes[node_index].x,
             self.visited_nodes[node_index].y)

            while True:

                if len(current_neighbour_nodes) <= 0:
                    node_index -= 1
                    break

                random_neighbour_node = current_neighbour_nodes.pop(random.randint(0,
                 len(current_neighbour_nodes) - 1))
                
                if random_neighbour_node in self.visited_nodes: continue

                self.remove_walls(self.visited_nodes[node_index], random_neighbour_node)


                self.visited_nodes.append(random_neighbour_node)
                node_index = len(self.visited_nodes) - 1
                break

        return self.maze
