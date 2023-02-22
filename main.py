from aamaze.base_maze import Maze
from aamaze.generation.eller import EllersGenerationAlgorithm
from aamaze.generation.kruskals import KruskalsGenerationAlgorithm
from aamaze.generation.prims import PrimsGenerationAlgorithm
from aamaze.generation.recursive_backtracker import \
    RecursiveBacktrackerAlgorithm
from aamaze.graphics.draw_maze import GraphicsApp
from aamaze.solving.dijkstra import DijkstraSolvingAlgorithm
from aamaze.solving.flood_fill import FloodFillSolutionCheck


def run():
    test_maze = Maze(16, 16)
    # EllersGenerationAlgorithm(test_maze).generate_maze()
    KruskalsGenerationAlgorithm(test_maze).generate_maze()
    # PrimsGenerationAlgorithm(test_maze).generate_maze()
    # RecursiveBacktrackerAlgorithm(test_maze).generate_maze()

    solution = DijkstraSolvingAlgorithm(test_maze)
    solution.solve_maze()



    app = GraphicsApp(test_maze, solution)
    app.run()


if __name__ == "__main__":
    run()
