from typing import Dict, List, Set

from src.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL,
                           GenerationAlgorithm, Maze, MazeNode)


class KruskalsGenerationAlgorithm(GenerationAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)

        self.walls: Set[str]  = self.get_all_walls(maze)
        self.node_index_sets: List[Set[int]] = self.get_individual_node_sets(maze)
    
    """TODO: Fix bug where rightmost nodes and topmost nodes always have no walls."""
    def generate_maze(self) -> Maze:

        while len(self.walls) > 0:

            current_wall = self.walls.pop()

            seperator_index = current_wall.find(",")
            node1_index = int(current_wall[:seperator_index])
            node2_index = int(current_wall[seperator_index + 1:])

            if node1_index not in self.node_index_sets[node1_index]:
                continue

            intersection = {node1_index}.intersection(self.node_index_sets[node2_index])

            if len({node1_index}.intersection(self.node_index_sets[node2_index])) == 0:
                self.node_index_sets[node2_index] = self.node_index_sets[node2_index].union(self.node_index_sets[node1_index])
                self.node_index_sets[node1_index] = set()
                self.remove_walls(self.maze.maze_body[node1_index], self.maze.maze_body[node2_index])
        
        print("Finished Maze Generation")

        return self.maze

    @staticmethod
    def remove_walls(current_node: MazeNode, neighbour_node: MazeNode):
        if neighbour_node.x > current_node.x:
            neighbour_node.walls &= 0b00001101
            current_node.walls &= 0b00001110
            return
        
        if neighbour_node.x < current_node.x:
            neighbour_node.walls &= 0b00001110
            current_node.walls &= 0b00001101
            return
        
        if neighbour_node.y > current_node.y:
            neighbour_node.walls &= 0b00001011
            current_node.walls &= 0b00000111
            return
        if neighbour_node.y < current_node.y:
            neighbour_node.walls &= 0b00000111
            current_node.walls &= 0b00001011
            return


    def get_all_walls(self, maze: Maze) -> Set[MazeNode]:
        maze_body = maze.maze_body

        walls = set()
        for node in maze_body:
            if node.walls & TOP_WALL and node.y > 0:
                walls.add(self.create_wall_string(node.x, node.y, node.x, node.y - 1, maze.w))
            if node.walls & LEFT_WALL and node.x > 0:
                walls.add(self.create_wall_string(node.x, node.y, node.x - 1, node.y, maze.w))
            
        return walls
    
    def get_individual_node_sets(self, maze: Maze) -> List[Set[str]]:
        node_sets = []
        for node in maze.maze_body:
            node_sets.append({node.x + (node.y * maze.w)})
        return node_sets
    
    def create_node_string(self, node: MazeNode):
        return f"{node.x} {node.y}"

    @staticmethod
    def create_wall_string(n1x: int, n1y: int, n2x: int, n2y: int, maze_width: int) -> str:
        if n1x > n2x or n1y > n2y:
            return f"{n2x + (n2y * maze_width)},{n1x + (n1y * maze_width)}"

        return f"{n1x + (n1y * maze_width)},{n2x + (n2y * maze_width)}"
