from aamaze.base_maze import Maze
from aamaze.generation.eller import Eller
from aamaze.generation.growing_tree import GrowingTree
from aamaze.generation.kruskals import Kruskals
from aamaze.generation.prims import Prims
from aamaze.generation.recursive_backtracker import RecursiveBacktracker
from aamaze.generation.recursive_divisior import RecursiveDivisor
from aamaze.generation.wilsons import Wilsons
from aamaze.graphics.app import GraphicsApp
from aamaze.solving.a_star import AStarSolver
from aamaze.solving.dijkstra import DijkstraSolver
from aamaze.solving.flood_fill import FloodFillSolutionCheck


def run():

    test_maze = Maze(32, 32, start_filled=True, entrance_index=0, exit_index=-1)
    # RecursiveDivisor(test_maze).generate_maze()
    # Eller(test_maze).generate_maze()
    # Kruskals(test_maze).generate_maze()
    # Prims(test_maze).generate_maze()
    # RecursiveBacktracker(test_maze).generate_maze()
    # Wilsons(test_maze).generate_maze()
    GrowingTree(test_maze, mode="random-newest-split-50").generate_maze()
    print("Generated Maze")


    # solution = FloodFillSolutionCheck(test_maze)


    solution = AStarSolver(test_maze)
    # solution = DijkstraSolvingAlgorithm(test_maze)-
    
    # solution.solve_maze()
    print(f"Solved Maze in {solution.step_counter} steps.")
    print(solution.solved)
    print(len(solution.solution))

    app = GraphicsApp(test_maze, solution)
    print(app.option_list)
    app.configure(show_step_counter=True, start_paused=True, target_steps_per_second=50)
    app.run()


if __name__ == "__main__":
    run()
