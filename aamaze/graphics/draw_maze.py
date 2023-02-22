from typing import List, Union

import pygame

from aamaze.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL,
                              Maze, MazeNode, SolvingAlgorithm)

TARGET_ASPECT_RATIO = [16, 9]
TARGET_WINDOW_WIDTH = 1280
TARGET_FPS = 60
TARGET_MONITOR_NUM = 1

WALL_COLOUR = [32, 160, 32]
SOLUTION_TILE_COLOUR = [32, 32, 160]
BACKGROUND_COLOUR = [4, 4, 4]

pygame.init()



class GraphicsApp:
    def __init__(self, maze: Maze, maze_solver: SolvingAlgorithm) -> None:
        self.maze = maze
        self.maze_solver = maze_solver
        window_size = self._get_window_size()
        print(f"window_size={window_size}")
        self.window = pygame.display.set_mode(window_size)
        self.running = True
    
        self._clock = pygame.time.Clock()
        self._events = List[pygame.event.Event]
    
    def _get_window_size(self) -> List[int]:
        monitor_size = pygame.display.get_desktop_sizes()[TARGET_MONITOR_NUM - 1]

        width = min(TARGET_WINDOW_WIDTH, int(monitor_size[0] * 9 / 10 ))

        return [int(width),
             int(width / TARGET_ASPECT_RATIO[0] * TARGET_ASPECT_RATIO[1])]

    def run(self):
        while self.running:
            if self.maze_solver: DrawMaze.draw_maze(self.window, self.maze, self.maze_solver.solution)
            else: DrawMaze.draw_maze(self.window, self.maze, None)

            self.event_loop()
            pygame.display.update()
            self.window.fill(BACKGROUND_COLOUR)

    
    def event_loop(self):
        self._events = pygame.event.get()
        for event in self._events:
            if event.type == pygame.QUIT:
                self.running = False
    


class DrawMaze:
    
    @classmethod
    def draw_maze_solution(cls, surface: pygame.surface.Surface, maze: Maze, solution: List[MazeNode]):
        tile_size = cls._get_tile_size(maze.w, maze.h, surface.get_width(),
         surface.get_height())

        wall_width = cls._get_wall_width(tile_size)

        solution_circle_size = max((tile_size - wall_width) // 3, 1)

        for node in solution:
            position = [node.x * tile_size + ((tile_size + wall_width) // 2), surface.get_height() - ((node.y + 1) * tile_size) + ((tile_size - wall_width) // 2)]
            pygame.draw.circle(surface, SOLUTION_TILE_COLOUR, position, solution_circle_size)

    @classmethod
    def draw_maze(cls, window: pygame.surface.Surface, maze: Maze, solution: Union[None, List[MazeNode]]):
        tile_size = cls._get_tile_size(maze.w, maze.h, window.get_width(),
         window.get_height())

        wall_width = cls._get_wall_width(tile_size)

        maze_draw_offset = [cls.get_draw_offset_1D(window.get_width(), maze.w, tile_size, wall_width),
                            -cls.get_draw_offset_1D(window.get_height(), maze.h, tile_size, wall_width)]

        
        draw_surface = pygame.Surface([window.get_width() - maze_draw_offset[0] + 1, window.get_height()])


        for node in maze.maze_body:
            if node.walls & TOP_WALL: 
                cls.draw_top_wall(draw_surface, node.x, node.y, wall_width, tile_size)
            if node.walls & BOTTOM_WALL : 
                cls.draw_bottom_wall(draw_surface, node.x, node.y, wall_width, tile_size)
            if node.walls & LEFT_WALL: 
                cls.draw_left_wall(draw_surface, node.x, node.y, wall_width, tile_size)
            if node.walls & RIGHT_WALL: 
                cls.draw_right_wall(draw_surface, node.x, node.y, wall_width, tile_size)   
        
        if solution:
            cls.draw_maze_solution(draw_surface, maze, solution)


        window.blit(draw_surface, maze_draw_offset) 



    @staticmethod
    def draw_top_wall(window: pygame.Surface, x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size + wall_width, window.get_height() - ((y + 1) * tile_size) - wall_width]
        wall_dimensions = [tile_size - wall_width, wall_width]

        pygame.draw.rect(window, WALL_COLOUR, [*position, *wall_dimensions])

    @staticmethod
    def draw_bottom_wall(window: pygame.Surface, x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size + wall_width, window.get_height() - (y * tile_size) - wall_width]
        wall_dimensions = [tile_size - wall_width, wall_width]

        pygame.draw.rect(window, WALL_COLOUR, [*position, *wall_dimensions])
    
    @staticmethod
    def draw_left_wall(window: pygame.Surface, x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size, window.get_height() - ((y + 1) * tile_size)]
        wall_dimensions = [wall_width, tile_size - wall_width]

        pygame.draw.rect(window, WALL_COLOUR, [*position, *wall_dimensions])

    @staticmethod
    def draw_right_wall(window: pygame.Surface, x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size + tile_size, window.get_height() - (y + 1) * tile_size]
        wall_dimensions = [wall_width, tile_size - wall_width]

        pygame.draw.rect(window, WALL_COLOUR, [*position, *wall_dimensions])


    @staticmethod
    def _get_tile_size(maze_width: int, maze_height: int,
     window_width: int, window_height: int) -> int:
        enforced_padding = max(4, 32 - min(2 * maze_width, 2 * maze_height))
        
        return max(6, (int(min((window_width - enforced_padding) / maze_width,
         (window_height - enforced_padding) / maze_height))))

    @staticmethod
    def _get_wall_width(tile_size: int) -> int:
        return max(2, (tile_size // 16) * 2)

    @staticmethod
    def get_draw_offset_1D(window_dimension_size: int, maze_dimension_size: int, tile_size: int, wall_width: int) -> int:
        return (window_dimension_size - (maze_dimension_size * tile_size) - wall_width) // 2
