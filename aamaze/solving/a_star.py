from __future__ import annotations

from typing import List

from aamaze.base_maze import Maze, MazeNode, SolvingAlgorithm


class AStarSolver(SolvingAlgorithm):
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

        self.path_nodes: List[PathNode]
        self.open_nodes: List[PathNode]
        self.closed_nodes: List[PathNode]

        self.current_node: PathNode
        self.start_node_index = self.maze.entrance_node.x + (self.maze.entrance_node.y * self.maze.w)
        self.target_node_index = self.maze.exit_node.x + (self.maze.exit_node.y * self.maze.w)
        self.target_node: PathNode

        self.setup_data_structures()

    
    def setup_data_structures(self):
        self.path_nodes = self.get_open_nodes_list()

        self.current_node = self.path_nodes[self.start_node_index]
        self.path_nodes[self.start_node_index].g_value = 0

        self.open_nodes = [self.current_node]
        self.closed_nodes = []
        self.solution = []
        self.step_counter = 0
        self.solved = False

        self.target_node = self.path_nodes[self.target_node_index]

    def solve_maze(self) -> List[MazeNode]:
        while not self.solved and len(self.open_nodes) > 0:
            self.step()

        return self.solution

    def step(self):
        if self.solved: return
        self.step_counter += 1
        
        self.current_node = self.get_lowest_f_value_node()

        if self.current_node is None:
            self._set_solved()
            return

        self.open_nodes.remove(self.current_node)
        self.closed_nodes.append(self.current_node)

        if self.maze.get_node_index(self.current_node.node) == self.target_node_index:
            self._set_solved()
            return
    
        neighbours = [self.get_path_node(maze_node) for maze_node in self.maze.get_node_neighbours(self.current_node.node)]

        for neighbour in neighbours:
            if neighbour.f_value <= self.current_node.f_value: continue
            if self.maze.check_nodes_seperated_by_wall(self.current_node.node, neighbour.node): continue
            if neighbour in self.closed_nodes: continue

            neighbour.g_value = self.calculate_g_value(self.current_node)
            neighbour.previous_node = self.current_node

            if neighbour not in self.closed_nodes: self.open_nodes.append(neighbour)
  
    def get_incomplete_solution_nodes(self) -> List[MazeNode]:
        return [path_node.node for path_node in self.closed_nodes]


    def _set_solved(self) -> bool:
        if self.current_node is None:
            self.solved = False
            return []

        if self.maze.get_node_index(self.current_node.node) == self.target_node_index:
            self.solved = True

        solution_node = self.target_node
        while solution_node is not None:
            self.solution.append(solution_node.node)
            solution_node = solution_node.previous_node
        

        self.solution.reverse()
        return self.solved
        

    def get_path_node(self, maze_node: MazeNode) -> PathNode:
        for path_node in self.path_nodes:
            if path_node.node == maze_node: return path_node

    def get_open_nodes_list(self):
        return [PathNode(self.maze[node_index], None, 999999, self.calculate_h_value(node_index)) for node_index in range(self.maze.size)]
    
    def get_lowest_f_value_node(self) -> PathNode:
        l_value = 99999999
        l_node: PathNode = None
        for path_node in self.open_nodes:
            if path_node.f_value < l_value:
                l_value = path_node.f_value
                l_node = path_node
        
        return l_node

    def calculate_h_value(self, node_index: int):
        return (abs((self.target_node_index % self.maze.w) - node_index % self.maze.w) +
         abs((self.target_node_index // self.maze.w) - node_index // self.maze.w))
    
    def calculate_g_value(self, previous_node: PathNode):
        return previous_node.g_value + 1


class PathNode:
    def __init__(self, node: MazeNode, previous_node: MazeNode, g_value: int = 0,
     h_value: int = 0) -> None:
        self.node = node
        self.previous_node = previous_node

        self.g_value: int = g_value
        self.h_value: int = h_value

    @property
    def f_value(self) -> int:
        return self.g_value + self.h_value
    
    def __repr__(self) -> str:
        return f"PathNode(node={self.node}, previous_node={self.previous_node}, f_value={self.f_value}, g_value={self.g_value}, h_value={self.h_value})"
