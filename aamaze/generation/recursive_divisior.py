import random
from typing import List

from aamaze.base_maze import GenerationAlgorithm, Maze, MazeNode


class RecursiveDivisor(GenerationAlgorithm):
    def __init__(self, maze: Maze) -> None:
        super().__init__(maze)
    
    def generate_maze(self) -> Maze:
        self.bisect_area(self.maze.maze_body, self.maze.w, self.maze.h)
    
    @classmethod
    def bisect_area(cls, maze: List[MazeNode], width: int, height: int):

        if width == 2 and height > 2:
            cls._bisect_maze_in_x_plane(maze, width, height)
            return 
        if height == 2 and width > 2:
            cls._bisect_maze_in_y_plane(maze, width, height)
            return 


        if random.randint(0, 1):
            cls._bisect_maze_in_y_plane(maze, width, height)
        else:
            cls._bisect_maze_in_x_plane(maze, width, height)


    @classmethod
    def _bisect_maze_in_x_plane(cls, maze: List[MazeNode], width: int, height: int):
        if height <= 1: return
        area_1 = maze[ :(height // 2) * width]
        area_2 = maze[(height // 2) * width: ]

        h1 = height // 2

        for i in range((h1 - 1) * width, h1* width): 
            cls.add_walls(maze[i], maze[i + width])
        
        opening_index = (h1 * width) + random.randint(0, width - 1)
        cls.remove_walls(maze[opening_index], maze[opening_index - width])

        cls.bisect_area(area_1, width, h1)
        cls.bisect_area(area_2, width, height - h1)
    
    @classmethod
    def _bisect_maze_in_y_plane(cls, maze: List[MazeNode], width: int, height: int):
        if width <= 1: return
        area_1 = [maze[x + (y * width)] for y in range(height) for x in range(0, width // 2) ]
        area_2 = [maze[x + (y * width)] for y in range(height) for x in range(width // 2, width)]

        w1 = width // 2

        for i in range(w1, width * height, width): 
            cls.add_walls(maze[i], maze[i - 1])

        opening_index = w1 - 1 + (random.randint(0, height - 1) * width)
        cls.remove_walls(maze[opening_index], maze[opening_index + 1])

        cls.bisect_area(area_1, w1, height)
        cls.bisect_area(area_2, width - w1, height)
