import random
from typing import Dict, List

from aamaze.base_maze import GenerationAlgorithm, Maze, MazeNode


class Prims(GenerationAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)

        self.visited_nodes: List[int] = []
        self.visit_status: Dict[int, bool] = self.generate_visit_status_dict(self.maze.size)

    
    def generate_maze(self) -> Maze:
        self.visited_nodes.append(random.randint(0, self.maze.size - 1))
        self.visit_status[self.visited_nodes[-1]] = True

        while len(self.visited_nodes) < self.maze.size:
            adjacent_node_indexes = self.get_adjacent_nodes()

            self.visited_nodes.append(adjacent_node_indexes[random.randint(0, len(adjacent_node_indexes) - 1)])
            self.visit_status[self.visited_nodes[-1]] = True

            new_node_neighbours = self.maze.get_neighbours_from_coordinates(self.visited_nodes[-1] % self.maze.w,
             self.visited_nodes[-1] // self.maze.w)
            random.shuffle(new_node_neighbours)
            
            for neighbour in new_node_neighbours:
                if self.visit_status[neighbour.x + (neighbour.y * self.maze.w)]:
                    self.remove_walls(self.maze[self.visited_nodes[-1]], neighbour)
                    break
        
        return self.maze
            

    
    @staticmethod
    def generate_visit_status_dict(num_nodes: int) -> Dict[int, bool]:
        return {index: False for index in range(0, num_nodes)}
    
    def get_adjacent_nodes(self):
        output = []

        for node_index in self.visited_nodes:
            neighbours = self.maze.get_neighbours_from_coordinates(node_index % self.maze.w, node_index // self.maze.w)
            for neighbour in neighbours:
                if not self.visit_status[neighbour.x + (neighbour.y * self.maze.w)]: 
                    output.append(neighbour.x + (neighbour.y * self.maze.w))
            
        return output
