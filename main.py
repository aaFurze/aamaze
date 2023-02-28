import time

from aamaze.base_maze import Maze
from aamaze.generation.eller import EllersGenerationAlgorithm
from aamaze.generation.kruskals import KruskalsGenerationAlgorithm
from aamaze.generation.prims import PrimsGenerationAlgorithm
from aamaze.generation.recursive_backtracker import \
    RecursiveBacktrackerAlgorithm
from aamaze.generation.recursive_divisior import \
    RecursiveDivisorGenerationAlgorithm
from aamaze.graphics.draw_maze import GraphicsApp
from aamaze.solving.a_star import AStarSolvingAlgorithm
from aamaze.solving.dijkstra import DijkstraSolvingAlgorithm
from aamaze.solving.flood_fill import FloodFillSolutionCheck


def run():
    test_maze = Maze(100, 64, start_filled=False)
    RecursiveDivisorGenerationAlgorithm(test_maze).generate_maze()
    # EllersGenerationAlgorithm(test_maze).generate_maze()
    # KruskalsGenerationAlgorithm(test_maze).generate_maze()
    # PrimsGenerationAlgorithm(test_maze).generate_maze()
    # RecursiveBacktrackerAlgorithm(test_maze).generate_maze()
    print("Generated Maze")


    solution = FloodFillSolutionCheck(test_maze)
    #solution.solve_maze()

    #solution = AStarSolvingAlgorithm(test_maze)
    

    print(f"Solved Maze in {solution.step_counter} steps.")
    print(solution.solved)
    print(len(solution.solution))

    app = GraphicsApp(test_maze, solution)
    app.run()


if __name__ == "__main__":
    run()
