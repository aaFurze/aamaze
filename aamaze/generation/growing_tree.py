import random
from typing import List, Union

from aamaze.base_maze import GenerationAlgorithm, Maze, MazeNode


class GrowingTreeGenerationAlgorithm(GenerationAlgorithm):
    def __init__(self, maze: Maze, mode: str = "random") -> None:
        super().__init__(maze)

        self.node_selection_mode: str = mode

        self.custom_selection_value: int = self._get_custom_selection_value()

        self.working_nodes: List[MazeNode]
        self.visited_nodes: List[MazeNode]
    
    def generate_maze(self) -> Maze:
        self.working_nodes = [random.choice(self.maze.maze_body)]
        self.visited_nodes = [self.working_nodes[0]]

        while len(self.working_nodes) > 0:
            current_node = self.get_node()
            neighbours = self.maze.get_node_neighbours(current_node)
            unvisited_neighbours = [neighbour for neighbour in neighbours if neighbour not in self.visited_nodes]

            if len(unvisited_neighbours) == 0: 
                self.working_nodes.remove(current_node)
                continue

            random_neighbour = random.choice(unvisited_neighbours)
            self.working_nodes.append(random_neighbour)
            self.visited_nodes.append(random_neighbour)
            self.remove_walls(current_node, random_neighbour)


    def get_node(self):
        if self.node_selection_mode == "random":
            return self.get_random_node(self.working_nodes)

        if self.node_selection_mode == "newest":
            return self.get_newest_added_node(self.working_nodes)
        
        if self.node_selection_mode.find("random-newest-split-") != -1:
            return self.get_random_newest_split_node(self.working_nodes, self.custom_selection_value)
        
        raise ValueError(f"\"{self.node_selection_mode}\" is not a valid mode")

    @staticmethod
    def get_random_node(nodes: List[MazeNode]) -> MazeNode:
        return random.choice(nodes)

    @staticmethod
    def get_newest_added_node(nodes: List[MazeNode]) -> MazeNode:
        return nodes[-1]
    
    @classmethod
    def get_random_newest_split_node(cls, nodes: List[MazeNode], split_value: int) -> MazeNode:
        rand_num: int = random.randrange(0, 100)
        if rand_num > split_value:
            return cls.get_random_node(nodes)
        return cls.get_newest_added_node(nodes)


    def _get_custom_selection_value(self):
        number_str: str = ""

        if self.node_selection_mode.find("random-newest-split-") != -1:
            for char in self.node_selection_mode[self.node_selection_mode.find("random-newest-split-") + 20:]:
                if char.isnumeric:
                    number_str += char
        if len(number_str) == 0: return 0

        return int(number_str)

        



