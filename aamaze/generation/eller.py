from __future__ import annotations

import random
from typing import Any, Dict, List, Set, Union

from aamaze.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL,
                              GenerationAlgorithm, Maze, MazeNode)


class EllersGenerationAlgorithm(GenerationAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)
    
    """
    TODO: Final row is currently just all set to blank nodes (no walls).
    """

    def generate_maze(self) -> Maze:
        y = 0

        current_row_node_sets: List[MutableSet[int]] = []

        while y + 1 < self.maze.size:
            current_row_node_sets = []
            # increment by 1
            x = 0
            # Create individual sets for first row.
            while x < self.maze.w:
                current_row_node_sets.append(MutableSet(self.maze[x + y].x + (self.maze[x + y].y * self.maze.w)))
                x += 1
            
            # For each set (barring first)
            for x in range(1, len(current_row_node_sets)):
                # If are not same set.
                if current_row_node_sets[x] is not current_row_node_sets[x - 1]:
                    # If == 1: Merge sets and remove walls between nodes.
                    if random.randint(0, 2):
                        current_row_node_sets[x] = current_row_node_sets[x - 1].union(current_row_node_sets[x])     
                        self.remove_walls(self.maze[x + y], self.maze[y + x - 1])  
            

            sets_checked_ids = []

            if y + self.maze.w >= self.maze.size:
                for i in range(self.maze.size - self.maze.w, self.maze.size - 1):
                    self.remove_walls(self.maze[i], self.maze[i - 1])
                    self.remove_walls(self.maze[i], self.maze[i + 1])

                
                break
                    

                    
            # For each set in current node, make a 
            for c_node_set in current_row_node_sets:
                # Prevent duplicate calls.
                if id(c_node_set) in sets_checked_ids: continue
                sets_checked_ids.append(id(c_node_set))

                # Pick a random node in the set.
                random_node_id = list(c_node_set)[random.randint(0, len(c_node_set) - 1)]
                above_node_id = random_node_id + self.maze.w
                self.remove_walls(self.maze[random_node_id], self.maze[above_node_id])
    
            y += self.maze.w 


        return self.maze



class MutableSet:
    def __init__(self, value: Union[set, Any]) -> None:
        self.value = value
        if type(self.value) is not set:
            self.value = {value}
    
    def __eq__(self, __o: object) -> bool:
        if hasattr(__o, "value"): return self.value == __o.value
        return False
    
    def __len__(self):
        return len(self.value)
    
    def union(self, other: Union[set, MutableSet]):
        if type(other) is set: self.value = self.value.union(other) 
        if type(other) is MutableSet: self.union(other.value)

        return self
    
    def __iter__(self):
        return iter(list(self.value))
    
    def __repr__(self):
        return f"MutableSet({self.value})"
    
    def remove(self, value: Any):
        self.value.remove(value)
    
    def intersection(self, other_set: Union[MutableSet, set]) -> Union[MutableSet, set]:
        if type(other_set) is MutableSet: return MutableSet(self.value.intersection(other_set.value))
        if type(other_set) is set: return self.value.intersection(other_set)
