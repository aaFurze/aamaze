from __future__ import annotations

from typing import List, Union

import pygame

from aamaze.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL,
                              Maze, MazeNode, SolvingAlgorithm)

TARGET_ASPECT_RATIO = [16, 9]
TARGET_WINDOW_WIDTH = 1280
TARGET_FPS = 60
TARGET_MONITOR_NUM = 1

WALL_COLOUR = [32, 160, 32]
SOLUTION_TILE_COLOUR = [32, 32, 240]
BACKGROUND_COLOUR = [240, 250, 250]

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
        draw_properties = DrawProperties()
        draw_properties.configure_properties(self.window, self.maze)

        while self.running:
            draw_properties.surface.fill(BACKGROUND_COLOUR)

            DrawMaze.draw_maze(self.maze, draw_properties)

            if self.maze_solver: 
                if self.maze_solver.solved:
                    DrawMaze.draw_maze_solution(self.maze_solver.solution, draw_properties)
                else:
                    self.maze_solver.step()
                    DrawMaze.draw_maze_solution(self.maze_solver.get_incomplete_solution_nodes(), draw_properties)
            
            self.window.blit(draw_properties.surface, draw_properties.surface_offset) 


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
    def draw_maze_solution(cls, solution: List[MazeNode], draw_properties: DrawProperties):

        solution_circle_size = max((draw_properties.tile_size - draw_properties.wall_width) // 3, 1)
        for node in solution:
            position = [node.x * draw_properties.tile_size + ((draw_properties.tile_size + draw_properties.wall_width) // 2),
             draw_properties.surface.get_height() - ((node.y + 1) * draw_properties.tile_size) + ((draw_properties.tile_size - draw_properties.wall_width) // 2)]
            pygame.draw.circle(draw_properties.surface, SOLUTION_TILE_COLOUR, position, solution_circle_size)

    @classmethod
    def draw_maze(cls, maze: Maze, draw_properties: DrawProperties):

        for node in maze.maze_body:
            if node.walls & TOP_WALL: 
                cls.draw_top_wall(draw_properties.surface, node.x, node.y, draw_properties.wall_width, draw_properties.tile_size)
            if node.walls & BOTTOM_WALL : 
                cls.draw_bottom_wall(draw_properties.surface, node.x, node.y, draw_properties.wall_width, draw_properties.tile_size)
            if node.walls & LEFT_WALL: 
                cls.draw_left_wall(draw_properties.surface, node.x, node.y, draw_properties.wall_width, draw_properties.tile_size)
            if node.walls & RIGHT_WALL: 
                cls.draw_right_wall(draw_properties.surface, node.x, node.y, draw_properties.wall_width, draw_properties.tile_size)   



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



class DrawProperties:
    def __init__(self) -> None:
        self.tile_size: int
        self.wall_width: int
        self.surface_offset: List[int]
        self.surface: pygame.surface.Surface

    def configure_properties(self, window: pygame.surface.Surface, maze: Maze):
        self.tile_size = self._get_tile_size(maze.w, maze.h, window.get_width(),
         window.get_height())

        self.wall_width = self._get_wall_width(self.tile_size)

        self.surface_offset = [self.get_draw_offset_1D(window.get_width(), maze.w, self.tile_size, self.wall_width),
                            -self.get_draw_offset_1D(window.get_height(), maze.h, self.tile_size, self.wall_width)]

        
        self.surface = pygame.Surface([window.get_width() - self.surface_offset[0] + 1, window.get_height()])


    @staticmethod
    def _get_tile_size(maze_width: int, maze_height: int, window_width: int, window_height: int) -> int:
        enforced_padding = max(4, 32 - min(2 * maze_width, 2 * maze_height))
        
        return max(6, (int(min((window_width - enforced_padding) / maze_width,
         (window_height - enforced_padding) / maze_height))))

    @staticmethod
    def _get_wall_width(tile_size: int) -> int:
        return max(2, (tile_size // 16) * 2)

    @staticmethod
    def get_draw_offset_1D(window_dimension_size: int, maze_dimension_size: int, tile_size: int, wall_width: int) -> int:
        return (window_dimension_size - (maze_dimension_size * tile_size) - wall_width) // 2
