from aamaze.base_maze import Maze
from aamaze.generation.eller import EllersGenerationAlgorithm
from aamaze.generation.growing_tree import GrowingTreeGenerationAlgorithm
from aamaze.generation.kruskals import KruskalsGenerationAlgorithm
from aamaze.generation.prims import PrimsGenerationAlgorithm
from aamaze.generation.recursive_backtracker import \
    RecursiveBacktrackerAlgorithm
from aamaze.generation.recursive_divisior import \
    RecursiveDivisorGenerationAlgorithm
from aamaze.generation.wilsons import WilsonsGenerationAlgorithm
from aamaze.graphics.app import GraphicsApp
from aamaze.solving.a_star import AStarSolvingAlgorithm
from aamaze.solving.dijkstra import DijkstraSolvingAlgorithm
from aamaze.solving.flood_fill import FloodFillSolutionCheck


def run():

    test_maze = Maze(32, 32, start_filled=True, entrance_index=0, exit_index=-30)
    # RecursiveDivisorGenerationAlgorithm(test_maze).generate_maze()
    EllersGenerationAlgorithm(test_maze).generate_maze()
    # KruskalsGenerationAlgorithm(test_maze).generate_maze()
    # PrimsGenerationAlgorithm(test_maze).generate_maze()
    # RecursiveBacktrackerAlgorithm(test_maze).generate_maze()
    # WilsonsGenerationAlgorithm(test_maze).generate_maze()
    # GrowingTreeGenerationAlgorithm(test_maze, mode="random-newest-split-50").generate_maze()
    print("Generated Maze")


    solution = FloodFillSolutionCheck(test_maze)


    # solution = AStarSolvingAlgorithm(test_maze)
    # solution = DijkstraSolvingAlgorithm(test_maze)-
    
    # solution.solve_maze()
    print(f"Solved Maze in {solution.step_counter} steps.")
    print(solution.solved)
    print(len(solution.solution))

    app = GraphicsApp(test_maze, solution)
    print(app.option_list)
    app.configure(show_step_counter=True, start_paused=True, target_steps_per_second=5)
    app.run()


if __name__ == "__main__":
    run()
