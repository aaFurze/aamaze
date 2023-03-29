import random
from typing import Dict, List

from aamaze.base_maze import Maze, MazeNode, SolvingAlgorithm


class DijkstraSolvingAlgorithm(SolvingAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)

        self.target_node_index: int
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
        self.step_counter = 0
        self.target_node_index = self.maze.exit_node.x + (self.maze.exit_node.y * self.maze.w)
        self.current_node_index = self.maze.entrance_node.x + (self.maze.entrance_node.y * self.maze.w)
        self.solved = False

    def solve_maze(self) -> List[MazeNode]:

        while self.current_node_index >= 0 and not self.solved:
            self.step()
        
        return self.solution


    def step(self):
        if self.solved: return
        self.step_counter += 1
         
        if self.current_node_index <= -1 or self.current_node_index == self.target_node_index: 
            self._set_solved()
            return

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

        self.current_node_index = self.get_nearest_node_index()


    def _set_solved(self) -> bool:
        if self.current_node_index != self.target_node_index:
            self.visit_statuses[self.current_node_index] = False
            self.solved = False
            return self.solved

        self.visit_statuses[self.current_node_index] = True
        self.node_paths[self.current_node_index] = self.node_paths[self.current_node_index] + [self.maze[self.current_node_index]]
        self.solution = self.node_paths[self.current_node_index]
        self.solved = True
        return self.solved

    def get_incomplete_solution_nodes(self) -> List[MazeNode]:
        node_indexes = [key for key in self.visit_statuses.keys() if self.visit_statuses[key]]
        return [self.maze[node_index] for node_index in node_indexes]

    def get_nearest_node_index(self):
        shortest_distance = 9999999
        nearest_index = -1
        for node_index in self.unvisited_nodes:
            if len(self.node_paths[node_index]) < shortest_distance and len(self.node_paths[node_index]) > 0:
                nearest_index = node_index
                shortest_distance = len(self.node_paths[node_index])
        
        return nearest_index
