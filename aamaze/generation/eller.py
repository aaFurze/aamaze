from __future__ import annotations

import random
from typing import Any, Dict, List, Set, Union

from aamaze.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL,
                              GenerationAlgorithm, Maze, MazeNode)


class EllersGenerationAlgorithm(GenerationAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)
    
    def generate_maze(self) -> Maze:
        row = 0

        node_dict: Dict[int, int] = {}

        while row < self.maze.h:
            
            self.remove_redundant_nodes(node_dict, row)
            self.add_nodes_to_dict(row, node_dict)

            # Create horizontal connections.
            for i in range(1, self.maze.w):
                # Don't make connections between nodes in the same set (already have path between them).
                if node_dict[i + (row * self.maze.w)] == node_dict[i - 1 + (row * self.maze.w)]: continue

                if random.randint(0, 2) > 0:
                    self.merge_nodes(node_dict, node_dict[i + (row * self.maze.w)], node_dict[i - 1 + (row * self.maze.w)])
                    self.remove_walls(self.maze[i + (row * self.maze.w)], self.maze[i - 1 + (row * self.maze.w)])
            
            row += 1

            # Do not make upwards connections on the final row (out of bounds error).
            # Instead, merge any remaining sets together to form one final set containing all MazeNode indexes.
            if row == self.maze.h:
                for i in range(1, self.maze.w):
                    if node_dict[i + ((row - 1) * self.maze.w)] != node_dict[i - 1 + ((row - 1) * self.maze.w)]:
                        self.merge_nodes(node_dict, node_dict[i + ((row - 1) * self.maze.w)], node_dict[i - 1 + ((row - 1) * self.maze.w)])
                        self.remove_walls(self.maze[i + ((row - 1) * self.maze.w)], self.maze[i - 1 + ((row - 1) * self.maze.w)])
                continue

            # Get Nodes which can be used to form an upwards connection and group them by their respective set
            # Need to be on correct row to be eligible.
            eligible_upward_nodes: Dict[int: List[int]] = {}

            for node_index in list(node_dict.keys()):
                if self.maze.w * row > node_index >= self.maze.w * (row - 1):
                    if not eligible_upward_nodes.get(node_dict[node_index]):
                        eligible_upward_nodes[node_dict[node_index]] = []
                    eligible_upward_nodes[node_dict[node_index]].append(node_index)

            # Make one upward connection for each Set.
            for key in list(eligible_upward_nodes.keys()):
                node = self.maze[random.choice(eligible_upward_nodes[key])]
                node_dict[node.x + ((node.y + 1) * self.maze.w)] = key
                self.remove_walls(node, self.maze[node.x + ((node.y + 1) * self.maze.w)])
            
            # Make random upward connections for each eligible MazeNode.
            for key in list(eligible_upward_nodes.keys()):
                for index in eligible_upward_nodes[key]:
                    if random.randint(0, 2): continue
                    node_dict[index + self.maze.w] = node_dict[index]
                    self.remove_walls(self.maze[index], self.maze[index + self.maze.w])
        

        self.create_entrance_and_exit()


        
    def add_nodes_to_dict(self, row: int, node_ids: Dict[int, int]):
        for i in range(self.maze.w):
            node_index = i + (row * self.maze.w)

            if node_ids.get(node_index, -1) == -1:
                node_ids[node_index] = node_index
        
    def merge_nodes(self, node_dict: Dict[int, int], index: int, other_index: int):
        keys = list(node_dict.keys())
        for key in keys:
            if node_dict[key] == other_index:
                node_dict[key] = index

    def remove_redundant_nodes(self, node_dict: Dict[int , int], row: int):
        for key in list(node_dict.keys()):
            if key < self.maze.w * (row - 2):
                node_dict.pop(key)
