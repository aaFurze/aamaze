from typing import Dict, List, Set

from aamaze.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL,
                              GenerationAlgorithm, Maze, MazeNode)


class KruskalsGenerationAlgorithm(GenerationAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)

        self.walls: Set[str]  = self.get_all_walls(maze)
        self.node_index_set_dict: Dict[int, int] = self.get_start_node_index_set_dict(maze)
        self.set_dict: Dict[int: set] = {}

    
    def generate_maze(self) -> Maze:
        
        while len(self.walls) > 0:
            current_wall = self.walls.pop()

            seperator_index = current_wall.find(",")
            node1_index = int(current_wall[:seperator_index])
            node2_index = int(current_wall[seperator_index + 1:])

            node1_set_index = self.node_index_set_dict[node1_index]
            node2_set_index = self.node_index_set_dict[node2_index]

            if node1_set_index == node2_set_index and node1_set_index != -1: continue

            if node1_set_index == -1 and node2_set_index == -1:
                new_set_index = len(self.set_dict.keys())
                self.set_dict[new_set_index] = {node1_index, node2_index}
                self.node_index_set_dict[node1_index] = new_set_index
                self.node_index_set_dict[node2_index] = new_set_index

            elif node1_set_index == -1:
                self.set_dict[node2_set_index].add(node1_index)
                self.node_index_set_dict[node1_index] = node2_set_index

            elif node2_set_index == -1:
                self.set_dict[node1_set_index].add(node2_index) 
                self.node_index_set_dict[node2_index] = node1_set_index

            else:
                self.set_dict[node1_set_index] = self.set_dict[node1_set_index].union(self.set_dict[node2_set_index])
                self.set_dict[node2_set_index] = None
                for key in self.node_index_set_dict.keys():
                    if self.node_index_set_dict[key] == node2_set_index: self.node_index_set_dict[key] = node1_set_index
                self.node_index_set_dict[node2_index] = node1_set_index
            
            self.remove_walls(self.maze[node1_index], self.maze[node2_index])
        
        return self.maze


    def get_start_node_index_set_dict(self, maze: Maze) -> Dict[int, int]:
        return {node_index: -1 for node_index in range(len(maze.maze_body))}


    def get_all_walls(self, maze: Maze) -> Set[MazeNode]:
        maze_body = maze.maze_body
        walls = set()
        for node in maze_body:
            if node.walls & TOP_WALL and node.y > 0:
                walls.add(self.create_wall_string(node.x, node.y, node.x, node.y - 1, maze.w))
            if node.walls & LEFT_WALL and node.x > 0:
                walls.add(self.create_wall_string(node.x, node.y, node.x - 1, node.y, maze.w))
            
        return walls

    @staticmethod
    def create_wall_string(n1x: int, n1y: int, n2x: int, n2y: int, maze_width: int) -> str:
        if n1x > n2x or n1y > n2y:
            return f"{n2x + (n2y * maze_width)},{n1x + (n1y * maze_width)}"

        return f"{n1x + (n1y * maze_width)},{n2x + (n2y * maze_width)}"
