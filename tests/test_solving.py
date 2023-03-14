import pytest

from aamaze.base_maze import Maze, MazeNode, SolvingAlgorithm
from aamaze.generation import (KruskalsGenerationAlgorithm,
                               RecursiveBacktrackerAlgorithm)
from aamaze.solving import (AStarSolvingAlgorithm, DijkstraSolvingAlgorithm,
                            FloodFillSolutionCheck)


@pytest.fixture(scope="module")
def kruskal_maze_32() -> Maze:
    maze = Maze(32, 32)
    KruskalsGenerationAlgorithm(maze).generate_maze()
    return maze

@pytest.fixture(scope="module")
def recursive_backtracker_maze_32() -> Maze:
    maze = Maze(32, 32)
    RecursiveBacktrackerAlgorithm(maze).generate_maze()
    return maze

@pytest.fixture(scope="module")
def kruskal_maze_8() -> Maze:
    maze = Maze(8, 8)
    KruskalsGenerationAlgorithm(maze).generate_maze()
    return maze

@pytest.fixture(scope="module")
def recursive_backtracker_maze_8() -> Maze:
    maze = Maze(8, 8)
    RecursiveBacktrackerAlgorithm(maze).generate_maze()
    return maze



@pytest.fixture(scope="module")
def kruskals_32_flood_filled(kruskal_maze_32) -> FloodFillSolutionCheck:
    flood_fill = FloodFillSolutionCheck(kruskal_maze_32)
    flood_fill.solve_maze()
    return flood_fill

@pytest.fixture(scope="module")
def recursive_backtracker_32_flood_filled(recursive_backtracker_maze_32) -> FloodFillSolutionCheck:
    flood_fill = FloodFillSolutionCheck(recursive_backtracker_maze_32)
    flood_fill.solve_maze()
    return flood_fill



solving_algorithms = [AStarSolvingAlgorithm,
                       DijkstraSolvingAlgorithm,
                       FloodFillSolutionCheck
                       ]



class TestCommonSolving:
    @pytest.mark.parametrize("index", [i for i in range(len(solving_algorithms))])
    def test_solve_kruskal_32_maze(self, kruskal_maze_32: Maze, index: int):
        solver: SolvingAlgorithm = solving_algorithms[index](kruskal_maze_32)
        solver.solve_maze()
        assert solver.solved

    @pytest.mark.parametrize("index", [i for i in range(len(solving_algorithms))])
    def test_solve_recursive_backtracker_32_maze(self, recursive_backtracker_maze_32: Maze, index: int):
        solver: SolvingAlgorithm = solving_algorithms[index](recursive_backtracker_maze_32)
        solver.solve_maze()
        assert solver.solved


    @pytest.mark.parametrize("index", [i for i in range(len(solving_algorithms))])
    def test_stepping_leads_to_solution_kruskals_8(self, kruskal_maze_8: Maze, index: int):
        solver: SolvingAlgorithm = solving_algorithms[index](kruskal_maze_8)
        while solver.step_counter < 1000 and not solver.solved: solver.step()
        
        assert solver.solved


    @pytest.mark.parametrize("index", [i for i in range(len(solving_algorithms))])
    def test_stepping_leads_to_solution_recursive_backtracker_8(self, recursive_backtracker_maze_8: Maze, index: int):
        solver: SolvingAlgorithm = solving_algorithms[index](recursive_backtracker_maze_8)
        while solver.step_counter < 1000 and not solver.solved: solver.step()
        
        assert solver.solved

    @pytest.mark.parametrize("index", [i for i in range(len(solving_algorithms))])
    def test_stepping_after_solved_does_nothing(self, recursive_backtracker_maze_8: Maze, index: int):
        solver: SolvingAlgorithm = solving_algorithms[index](recursive_backtracker_maze_8)
        solver.solve_maze()

        solver.step()
        stored_step_counter = solver.step_counter

        assert solver.solved
        assert solver.step_counter == stored_step_counter

    @pytest.mark.parametrize("index, maze_size", [[i, j] for i in range(len(solving_algorithms)) for j in range(1, 3)])
    def test_solvers_work_on_small_maze(self, index: int, maze_size: int):
        maze = Maze(maze_size, maze_size)
        KruskalsGenerationAlgorithm(maze).generate_maze()
        solver: SolvingAlgorithm = solving_algorithms[index](maze)
        solver.solve_maze()

        assert solver.solved



class TestFloodFill:
    def test_all_tiles_visited_kruskals(self, kruskals_32_flood_filled: FloodFillSolutionCheck):
        assert len(kruskals_32_flood_filled.solution) == kruskals_32_flood_filled.maze.size

    def test_all_tiles_visited_recursive_backtracker(self, recursive_backtracker_32_flood_filled: FloodFillSolutionCheck):
        assert len(recursive_backtracker_32_flood_filled.solution) == recursive_backtracker_32_flood_filled.maze.size

    def test_flood_fill_percentage_equals_1_kruskals(self, kruskals_32_flood_filled: FloodFillSolutionCheck):
        assert kruskals_32_flood_filled.fill_percent == 1

    def test_flood_fill_percentage_equals_1_recursive_backtracker(self, recursive_backtracker_32_flood_filled: FloodFillSolutionCheck):
        assert recursive_backtracker_32_flood_filled.fill_percent == 1
