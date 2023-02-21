from src.base_maze import Maze
from src.generation.eller import EllersGenerationAlgorithm
from src.generation.kruskals import KruskalsGenerationAlgorithm
from src.generation.prims import PrimsGenerationAlgorithm
from src.generation.recursive_backtracker import RecursiveBacktrackerAlgorithm
from src.graphics.draw_maze import GraphicsApp
from src.solving.flood_fill import FloodFillSolutionCheck


def run():
    test_maze = Maze(32, 32)
    # EllersGenerationAlgorithm(test_maze).generate_maze()
    # KruskalsGenerationAlgorithm(test_maze).generate_maze()
    PrimsGenerationAlgorithm(test_maze).generate_maze()
    # RecursiveBacktrackerAlgorithm(test_maze).generate_maze()
    # print(len(FloodFillSolutionCheck(test_maze).solve_maze()))



    app = GraphicsApp(test_maze)
    app.run()


if __name__ == "__main__":
    run()
