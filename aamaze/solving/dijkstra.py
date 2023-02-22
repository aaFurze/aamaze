import random
from typing import Dict, List

from aamaze.base_maze import Maze, MazeNode, SolvingAlgorithm


class DijkstraSolvingAlgorithm(SolvingAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)

        self.unvisited_nodes = [index for index in range(0, len(self.maze.maze_body))]
        self.visit_statuses: Dict[int, bool] = self.generate_visit_statuses_dict(len(self.maze.maze_body))

        self.target_node_index = len(self.maze.maze_body) - 1

        self.node_paths: List[List[MazeNode]] = self.generate_start_path_dict(len(self.maze.maze_body))

        self.solved = False
        self.shortest_path: List[MazeNode] = []
    
    def solve_maze(self) -> List[MazeNode]:
        current_node_index = 0  # start node
        self.node_paths[current_node_index] = []

        while not self.solved:
            neighbours = self.maze.get_node_neighbours(self.maze.maze_body[current_node_index])

            for neighbour in neighbours:
                if self.maze.check_seperated_by_wall(self.maze.maze_body[current_node_index], neighbour): continue

                neighbour_index = self.maze.get_node_index(neighbour)
                if self.visit_statuses[neighbour_index]: continue

                new_distance = len(self.node_paths[current_node_index]) + 1
                if new_distance < len(self.node_paths[neighbour_index]) or len(self.node_paths[neighbour_index]) == 0: 
                    self.node_paths[neighbour_index] = self.node_paths[current_node_index] + [self.maze.maze_body[current_node_index]]
            
            self.visit_statuses[current_node_index] = True
            self.unvisited_nodes.remove(current_node_index)


            if current_node_index == self.target_node_index:
                self.node_paths[current_node_index] = self.node_paths[current_node_index] + [self.maze.maze_body[current_node_index]]
                self.shortest_path = self.node_paths[current_node_index]
                self.solved = True
            

            next_node_index = self.get_nearest_node_index_and_distance()

            if next_node_index == -1: break

            
            current_node_index = next_node_index


    def get_nearest_node_index_and_distance(self):
        shortest_distance = 9999999
        nearest_index = -1
        for node_index in self.unvisited_nodes:
            if len(self.node_paths[node_index]) < shortest_distance and len(self.node_paths[node_index]) > 0:
                nearest_index = node_index
                shortest_distance = len(self.node_paths[node_index])
        
        return nearest_index


    @staticmethod
    def generate_start_path_dict(num_nodes: int) -> Dict[int, int]:
        return [[] for _ in range(0, num_nodes)]
    
    @staticmethod
    def generate_visit_statuses_dict(num_nodes: int) -> Dict[int, bool]:
        return {key: False for key in range(0, num_nodes)}