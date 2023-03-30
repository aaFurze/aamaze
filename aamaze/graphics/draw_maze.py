from __future__ import annotations

import os
from typing import List

import pygame

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

pygame.init()

from aamaze.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL,
                              Maze, MazeNode, SolvingAlgorithm)
from aamaze.graphics.defaults import (DEFAULT_FPS_COUNTER_COLOUR,
                                      DEFAULT_FPS_COUNTER_SIZE,
                                      DEFAULT_FPS_FONT, DEFAULT_STEP_COLOUR,
                                      DEFAULT_STEP_SIZE)


class DrawMaze:
    @classmethod
    def draw_fps_counter(cls, window: pygame.Surface, ticks: int):
        fps = int(1000 / max(1, ticks))
        fps_surface = DEFAULT_FPS_FONT.render(f"FPS: {fps} ({int(ticks)}ms)", True, DEFAULT_FPS_COUNTER_COLOUR, [200, 200, 200])
        window.blit(fps_surface, [window.get_width() - 180, DEFAULT_FPS_COUNTER_SIZE])
    
    @classmethod
    def draw_steps_per_second(cls, window: pygame.Surface, steps: int):
        step_surface = DEFAULT_FPS_FONT.render(f"Target Steps per Second: {steps}", True, DEFAULT_STEP_COLOUR, [200, 200, 200])
        window.blit(step_surface, [window.get_width() - 240, DEFAULT_STEP_SIZE * 2.5])
    
    @classmethod
    def draw_maze(cls, maze: Maze, draw_properties: DrawProperties):

        surface = draw_properties.surface
        wall_colour = draw_properties.wall_colour
        wall_width = draw_properties.wall_width
        tile_size = draw_properties.tile_size

        for node in maze.maze_body:
            if node.walls & TOP_WALL: 
                cls._draw_top_wall(surface, wall_colour, node.x, node.y, wall_width, tile_size)
            if node.walls & BOTTOM_WALL : 
                cls._draw_bottom_wall(surface, wall_colour, node.x, node.y, wall_width, tile_size)
            if node.walls & LEFT_WALL: 
                cls._draw_left_wall(surface, wall_colour, node.x, node.y, wall_width, tile_size)
            if node.walls & RIGHT_WALL: 
                cls._draw_right_wall(surface, wall_colour, node.x, node.y, wall_width, tile_size)   
        
        cls._draw_end(surface, draw_properties.entrance_colour, maze.entrance_node.x - 1, maze.entrance_node.y,
                        wall_width, tile_size)
        cls._draw_end(surface, draw_properties.exit_colour, maze.exit_node.x - 1, maze.exit_node.y,
                        wall_width, tile_size)
    
    @classmethod
    def draw_maze_solution(cls, maze_solver: SolvingAlgorithm, draw_properties: DrawProperties):
        if maze_solver.solved:
            DrawMaze._draw_maze_solution_path(maze_solver.solution, draw_properties)
        else:
            DrawMaze._draw_maze_solution_path(maze_solver.get_incomplete_solution_nodes(), draw_properties)



    @classmethod
    def _draw_maze_solution_path(cls, solution: List[MazeNode], draw_properties: DrawProperties):

        solution_circle_size = max((draw_properties.tile_size - draw_properties.wall_width) // 3, 2)
        for node in solution:
            position = [node.x * draw_properties.tile_size + ((draw_properties.tile_size + draw_properties.wall_width) // 2),
             draw_properties.surface.get_height() - ((node.y + 1) * draw_properties.tile_size) + ((draw_properties.tile_size - draw_properties.wall_width) // 2)]
            pygame.draw.circle(draw_properties.surface, draw_properties.solution_colour, position, solution_circle_size)


    @staticmethod
    def _draw_top_wall(window: pygame.Surface, wall_colour: List[int], x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size + wall_width, window.get_height() - ((y + 1) * tile_size) - wall_width]
        wall_dimensions = [tile_size - wall_width, wall_width]

        pygame.draw.rect(window, wall_colour, [*position, *wall_dimensions])

    @staticmethod
    def _draw_bottom_wall(window: pygame.Surface, wall_colour: List[int], x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size + wall_width, window.get_height() - (y * tile_size) - wall_width]
        wall_dimensions = [tile_size - wall_width, wall_width]

        pygame.draw.rect(window, wall_colour, [*position, *wall_dimensions])
    
    @staticmethod
    def _draw_left_wall(window: pygame.Surface, wall_colour: List[int], x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size, window.get_height() - ((y + 1) * tile_size)]
        wall_dimensions = [wall_width, tile_size - wall_width]

        pygame.draw.rect(window, wall_colour, [*position, *wall_dimensions])

    @staticmethod
    def _draw_right_wall(window: pygame.Surface, wall_colour: List[int], x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size + tile_size, window.get_height() - (y + 1) * tile_size]
        wall_dimensions = [wall_width, tile_size - wall_width]

        pygame.draw.rect(window, wall_colour, [*position, *wall_dimensions])


    @staticmethod
    def _draw_end(window: pygame.Surface, colour: List[int], x: int, y: int, wall_width: int, tile_size: int):
        position = [x * tile_size + tile_size + wall_width, (window.get_height() - (y + 1) * tile_size)]
        tile_dimensions = [tile_size - wall_width, tile_size - wall_width]
        pygame.draw.rect(window, colour, [*position, *tile_dimensions])



class DrawProperties:
    def __init__(self) -> None:
        self.tile_size: int
        self.wall_width: int
        self.surface_offset: List[int]
        self.surface: pygame.surface.Surface

        self.entrance_colour: List[int]
        self.exit_colour: List[int]
        self.solution_colour: List[int]
        self.wall_colour: List[int]

    def configure_properties(self, window: pygame.surface.Surface, maze: Maze,
                              entrance_colour: List[int], exit_colour: List[int],
                                solution_colour: List[int], wall_colour: List[int]):
        self.tile_size = self._get_tile_size(maze.w, maze.h, window.get_width(),
         window.get_height())

        self.wall_width = self._get_wall_width(self.tile_size)

        self.surface_offset = [self.get_draw_offset_1D(window.get_width(), maze.w, self.tile_size, self.wall_width),
                            -self.get_draw_offset_1D(window.get_height(), maze.h, self.tile_size, self.wall_width)]

        
        self.surface = pygame.Surface([window.get_width() - self.surface_offset[0] + 1, window.get_height()])

        self.entrance_colour = entrance_colour
        self.exit_colour = exit_colour
        self.solution_colour = solution_colour
        self.wall_colour = wall_colour


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
