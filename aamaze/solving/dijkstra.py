import random
from typing import Dict, List

from aamaze.base_maze import Maze, MazeNode, SolvingAlgorithm


class DijkstraSolvingAlgorithm(SolvingAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)

        self.target_node_index = self.maze.size - 1
        self.current_node_index: int

        self.unvisited_nodes: List[int]
        self.visit_statuses: Dict[int, bool]
        self.node_paths: List[List[MazeNode]]
        self.setup_data_structures()
    
    def setup_data_structures(self):
        self.unvisited_nodes = [index for index in range(0, self.maze.size)]
        self.visit_statuses = {key: False for key in range(0, self.maze.size)}
        self.node_paths = [[] for _ in range(0, self.maze.size)]
        self.solution = []

    def solve_maze(self) -> List[MazeNode]:
        self.current_node_index = 0  # start node
        self.node_paths[self.current_node_index] = []

        while self.current_node_index >= 0 and self.current_node_index != self.target_node_index:
            self.current_node_index = self.step()
        
        self._set_solved()
        return self.solution


    def step(self):
        if self.current_node_index <= -1: return -1
        if self.current_node_index == self.target_node_index:
            return self.current_node_index

        current_node = self.maze[self.current_node_index]
        current_node_neighbours = self.maze.get_node_neighbours(current_node)

        for neighbour in current_node_neighbours:
            if self.maze.check_nodes_seperated_by_wall(current_node, neighbour): continue

            neighbour_index = self.maze.get_node_index(neighbour)
            if self.visit_statuses[neighbour_index]: continue

            new_distance = len(self.node_paths[self.current_node_index]) + 1
            if new_distance < len(self.node_paths[neighbour_index]) or len(self.node_paths[neighbour_index]) == 0: 
                self.node_paths[neighbour_index] = self.node_paths[self.current_node_index] + [self.maze[self.current_node_index]]
        
        self.visit_statuses[self.current_node_index] = True
        self.unvisited_nodes.remove(self.current_node_index)

        return self.get_nearest_node_index_and_distance()


    def _set_solved(self) -> bool:
        self.node_paths[self.current_node_index] = self.node_paths[self.current_node_index] + [self.maze[self.current_node_index]]
        self.solution = self.node_paths[self.current_node_index]
        if self.current_node_index == self.target_node_index: self.solved = True
        else: self.solved = False
        return self.solved

    def get_nearest_node_index_and_distance(self):
        shortest_distance = 9999999
        nearest_index = -1
        for node_index in self.unvisited_nodes:
            if len(self.node_paths[node_index]) < shortest_distance and len(self.node_paths[node_index]) > 0:
                nearest_index = node_index
                shortest_distance = len(self.node_paths[node_index])
        
        return nearest_index
