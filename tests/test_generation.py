import pytest

from aamaze.base_maze import GenerationAlgorithm, Maze
from aamaze.generation import (KruskalsGenerationAlgorithm,
                               PrimsGenerationAlgorithm,
                               RecursiveBacktrackerAlgorithm)
from aamaze.solving import AStarSolvingAlgorithm, FloodFillSolutionCheck

algorithms = [
    KruskalsGenerationAlgorithm, PrimsGenerationAlgorithm,
    RecursiveBacktrackerAlgorithm
]

maze_sizes = [[21, 7], [16, 16], [3, 3], [1, 1], [3, 2], [1, 7], [13, 4]]


generation_algorithms_maze_sizes = [[algorithm, size] for algorithm in algorithms 
                                        for size in maze_sizes]



@pytest.fixture
def generation_algorithm_maze_size_pairs() -> list:
   return generation_algorithms_maze_sizes



class TestGenerationAlgorithms:
    @pytest.mark.parametrize("index", range(len(generation_algorithms_maze_sizes)))
    def test_mazes_solvable(self, generation_algorithm_maze_size_pairs, index: int):
        maze = Maze(*generation_algorithm_maze_size_pairs[index][1])
        maze_generator: GenerationAlgorithm = generation_algorithm_maze_size_pairs[index][0](maze)
        maze_generator.generate_maze()

        solver = AStarSolvingAlgorithm(maze)
        solver.solve_maze()

        assert solver.solved
    
    @pytest.mark.parametrize("index", range(len(generation_algorithms_maze_sizes)))
    def test_maze_solution_minimum_length(self, generation_algorithm_maze_size_pairs, index: int):
        maze = Maze(*generation_algorithm_maze_size_pairs[index][1])
        maze_generator: GenerationAlgorithm = generation_algorithm_maze_size_pairs[index][0](maze)
        maze_generator.generate_maze()

        solver = AStarSolvingAlgorithm(maze)
        solver.solve_maze()

        assert len(solver.solution) >= sum(generation_algorithm_maze_size_pairs[index][1]) - 1

    @pytest.mark.parametrize("index", range(len(generation_algorithms_maze_sizes)))
    def test_all_nodes_reachable(self, generation_algorithm_maze_size_pairs, index: int):
        maze = Maze(*generation_algorithm_maze_size_pairs[index][1])
        maze_generator: GenerationAlgorithm = generation_algorithm_maze_size_pairs[index][0](maze)
        maze_generator.generate_maze()

        solver = FloodFillSolutionCheck(maze)
        solver.solve_maze()

        assert solver.solved
