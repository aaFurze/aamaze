import pytest

from aamaze.base_maze import GenerationAlgorithm, Maze
from aamaze.generation import (Eller, GrowingTree, Kruskals, Prims,
                               RecursiveBacktracker, RecursiveDivisor, Wilsons)
from aamaze.solving import AStarSolver, FloodFillSolutionCheck

# Maze needs to start filled for algorithm to work.
start_filled_algorithms = [
    Kruskals, Prims,
    RecursiveBacktracker, Wilsons, GrowingTree, Eller
]
# Maze needs to start empty for algorithm to work.
start_empty_algorithms = [RecursiveDivisor]


algorithms = start_empty_algorithms + start_filled_algorithms


maze_sizes = [[21, 7], [16, 16], [3, 3], [1, 1], [3, 2], [1, 7], [13, 4]]

generation_algorithms_maze_sizes = [[algorithm, size, True] for algorithm in algorithms 
                                        for size in maze_sizes]

for algorithm in generation_algorithms_maze_sizes:
    if algorithm[0] in start_empty_algorithms: algorithm[2] = False



@pytest.fixture
def generation_algorithm_maze_size_pairs() -> list:
   return generation_algorithms_maze_sizes



class TestGenerationAlgorithms:
    @pytest.mark.parametrize("index", range(len(generation_algorithms_maze_sizes)))
    def test_mazes_solvable(self, generation_algorithm_maze_size_pairs, index: int):  
        maze = Maze(*generation_algorithm_maze_size_pairs[index][1], start_filled=generation_algorithm_maze_size_pairs[index][2])
        maze_generator: GenerationAlgorithm = generation_algorithm_maze_size_pairs[index][0](maze)
        maze_generator.generate_maze()

        solver = AStarSolver(maze)
        solver.solve_maze()

        assert solver.solved
    
    @pytest.mark.parametrize("index", range(len(generation_algorithms_maze_sizes)))
    def test_maze_solution_minimum_length(self, generation_algorithm_maze_size_pairs, index: int):  
        maze = Maze(*generation_algorithm_maze_size_pairs[index][1], start_filled=generation_algorithm_maze_size_pairs[index][2])
        maze_generator: GenerationAlgorithm = generation_algorithm_maze_size_pairs[index][0](maze)
        maze_generator.generate_maze()

        solver = AStarSolver(maze)
        solver.solve_maze()

        assert len(solver.solution) >= sum(generation_algorithm_maze_size_pairs[index][1]) - 1

    @pytest.mark.parametrize("index", range(len(generation_algorithms_maze_sizes)))
    def test_all_nodes_reachable(self, generation_algorithm_maze_size_pairs, index: int):
        maze = Maze(*generation_algorithm_maze_size_pairs[index][1], start_filled=generation_algorithm_maze_size_pairs[index][2])
        maze_generator: GenerationAlgorithm = generation_algorithm_maze_size_pairs[index][0](maze)
        maze_generator.generate_maze()

        solver = FloodFillSolutionCheck(maze)
        solver.solve_maze()

        assert solver.solved
