import random
from typing import List

from aamaze.base_maze import GenerationAlgorithm, Maze, MazeNode


class Wilsons(GenerationAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)
    
        self.unvisited_nodes: List[MazeNode]
        self.visited_nodes: List[MazeNode]
        self.current_nodes_checked: List[MazeNode]
        self.current_nodes_checked_paths: List[int]

    def generate_maze(self) -> Maze:

        self.unvisited_nodes = [index for index in range(len(self.maze.maze_body))]
        self.visited_nodes = []
        self.current_nodes_checked = []
        self.current_nodes_checked_paths = []

        self.visited_nodes.append(self.unvisited_nodes.pop(random.randint(0, len(self.unvisited_nodes) - 1)))

        while len(self.unvisited_nodes) > 0:
            current_node: MazeNode = random.choice(self.unvisited_nodes)
            self.current_nodes_checked = [current_node]
            self.current_nodes_checked_paths = ["i"]

            while self.current_nodes_checked[-1] not in self.visited_nodes:
                random_neighbour = self.get_random_neighbour_index(current_node, self.maze)

                try:
                    node_pos = self.current_nodes_checked.index(current_node)
                    self.current_nodes_checked_paths[node_pos] = self.get_direction_from_node(current_node, random_neighbour, self.maze)
                except ValueError:
                    self.current_nodes_checked.append(current_node)
                    self.current_nodes_checked_paths.append(self.get_direction_from_node(current_node, random_neighbour, self.maze))
                finally:
                    current_node = random_neighbour
            
            current_node = self.current_nodes_checked[0]
            current_direction = self.current_nodes_checked_paths[0]

            while True:

                if current_node == self.current_nodes_checked[-1]: break

                neighbour_node = self.get_neighbour_based_on_str(current_node, current_direction)
                self.remove_walls(self.maze[current_node], self.maze[neighbour_node])

                next_index = self.current_nodes_checked.index(neighbour_node)

                self.unvisited_nodes.remove(current_node)
                self.visited_nodes.append(current_node)

                current_node = self.current_nodes_checked[next_index]
                current_direction = self.current_nodes_checked_paths[next_index]
        



    def get_neighbour_based_on_str(self, node_index: int, direction: str):
        if direction == "l": return node_index - 1
        if direction == "r": return node_index + 1
        if direction == "t": return node_index + self.maze.w
        if direction == "b": return node_index - self.maze.w

        raise ValueError(f"Invalid value for direction ({direction}).")



    def get_random_neighbour_index(self, node_index: int, maze: Maze):
        neighbours = maze.get_node_neighbours(maze[node_index])
        random_neighbour = random.choice(neighbours)
        return random_neighbour.x + (random_neighbour.y * maze.w)

    @staticmethod
    def get_direction_from_node(node_index: int, other_node_index: int, maze: Maze):
        if other_node_index - node_index == -1: return "l"
        if other_node_index - node_index == 1: return "r"
        if other_node_index - node_index == maze.w: return "t"
        if other_node_index - node_index == - maze.w: return "b"

        raise ValueError(f"other_node_index is not a neighbour to node_index (node_index={node_index}, other_node_index={other_node_index}).")
