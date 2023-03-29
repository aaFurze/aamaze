from typing import List, Set

from aamaze.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL,
                              Maze, MazeNode, SolvingAlgorithm)


class FloodFillSolutionCheck(SolvingAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)

        self.fill_percent: float  # Value between 0 and 1 depending on how many nodes were visited in the maze.
        # Maze is solved if all nodes in the maze were visited else False

        self.visited_nodes: Set[MazeNode]
        self.unchecked_nodes: List[MazeNode]
        self.setup_data_structures()

    
    def setup_data_structures(self):
        self.visited_nodes = set()
        self.unchecked_nodes = []
        self.solution = []
        self.step_counter = 0
        self.fill_percent = 0
        self.sovled = False

        self.unchecked_nodes.append(self.maze.get_node_from_coordinates(0, 0))
        self.visited_nodes.add(self.unchecked_nodes[0])


    def solve_maze(self) -> List[MazeNode]:
        while len(self.unchecked_nodes) > 0 and not self.solved:
            self.step()

        return self.solution

    def step(self):
        if self.solved: return
        if len(self.unchecked_nodes) == 0: return
        self.step_counter += 1

        
        current_node = self.unchecked_nodes.pop(0)
        neighbours = self.maze.get_neighbours_from_coordinates(current_node.x, current_node.y)

        for neighbour_node in neighbours:
            if {neighbour_node}.issubset(self.visited_nodes): continue
            if self.maze.check_nodes_seperated_by_wall(current_node, neighbour_node): continue

            self.visited_nodes.add(neighbour_node)
            self.unchecked_nodes.append(neighbour_node)

        if len(self.unchecked_nodes) == 0: 
            self._set_solved()
            return

    def _set_solved(self) -> bool:
        self.fill_percent = len(self.visited_nodes) / self.maze.size
        if len(self.visited_nodes) == self.maze.size: self.solved = True
        else: self.solved = False

        self.solution = list(self.visited_nodes)

        return self.solved

    def get_incomplete_solution_nodes(self) -> List[MazeNode]:
        return list(self.visited_nodes)
