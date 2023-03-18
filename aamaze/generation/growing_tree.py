import random
from typing import List

from aamaze.base_maze import GenerationAlgorithm, Maze, MazeNode


class GrowingTreeGenerationAlgorithm(GenerationAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)

        self.working_nodes: List[MazeNode]
        self.visited_nodes: List[MazeNode]
    
    def generate_maze(self) -> Maze:
        self.working_nodes = [random.choice(self.maze.maze_body)]
        self.visited_nodes = [self.working_nodes[0]]

        while len(self.working_nodes) > 0:
            random_node = random.choice(self.working_nodes)
            neighbours = self.maze.get_node_neighbours(random_node)
            unvisited_neighbours = [neighbour for neighbour in neighbours if neighbour not in self.visited_nodes]

            if len(unvisited_neighbours) == 0: 
                self.working_nodes.remove(random_node)
                continue

            random_neighbour = self.choose_random_neighbour(unvisited_neighbours)
            self.working_nodes.append(random_neighbour)
            self.visited_nodes.append(random_neighbour)
            self.remove_walls(random_node, random_neighbour)

    @staticmethod
    def choose_random_neighbour(neighbours: List[MazeNode]):
        return random.choice(neighbours)

