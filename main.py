from src.base_maze import Maze
from src.graphics.draw_maze import GraphicsApp


def run():
    test_maze = Maze(64, 36)
    test_maze.get_node(3, 3).walls = 0b00000000
    test_maze.get_node(3, 2).walls = 0b00000000
    test_maze.get_node(2, 2).walls = 0b00000000
    app = GraphicsApp(test_maze)
    app.run()


if __name__ == "__main__":
    run()
