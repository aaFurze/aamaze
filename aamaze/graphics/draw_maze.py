from __future__ import annotations

import os
from typing import List

from aamaze.base_maze import (BOTTOM_WALL, LEFT_WALL, RIGHT_WALL, TOP_WALL,
                              Maze, MazeNode, SolvingAlgorithm)

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame

pygame.init()

TARGET_ASPECT_RATIO = [16, 9]
TARGET_WINDOW_WIDTH = 1280
TARGET_FPS = 60
TARGET_MONITOR_NUM = 1

WALL_COLOUR = [32, 160, 32]
SOLUTION_TILE_COLOUR = [32, 32, 240]
BACKGROUND_COLOUR = [240, 250, 250]
ENTRANCE_TILE_COLOUR = [40, 200, 40]
EXIT_TILE_COLOUR = [200, 40, 40]

FPS_COUNTER_COLOUR = [4, 4, 4]
FPS_COUNTER_SIZE = 24 
FPS_FONT = pygame.font.Font(None, FPS_COUNTER_SIZE)


STEP_COLOUR = [4, 4, 4]
STEP_SIZE = 24 
STEP_FONT = pygame.font.Font(None, STEP_SIZE)



class GraphicsApp:
    def __init__(self, maze: Maze, maze_solver: SolvingAlgorithm = None) -> None:
        self.maze = maze
        self.maze_solver = maze_solver

        self.window_size = self._get_window_size()
        self.window: pygame.Surface

        self.running = True
    
        self._clock = pygame.time.Clock()
        self._ticks: int = 0
        self._events = List[pygame.event.Event]

        self._step_calls_per_second = 50
        self._step_call_increment = 1000 / self._step_calls_per_second
        self._step_call_counter = 0
        self._run_steps = True

        self.k_space: bool
        self.k_s: bool
        self.k_r: bool
        self.k_plus: bool
        self.k_minus: bool

        self._reset_keys()


    def _get_draw_properties(self, window: pygame.Surface, maze: Maze) -> DrawProperties:
        output = DrawProperties()
        output.configure_properties(window, maze)
        return output
    
    def _late_display_update(self, draw_properties: DrawProperties):
        pygame.display.update()
        self.window.fill(BACKGROUND_COLOUR)
        draw_properties.surface.fill(BACKGROUND_COLOUR)

    def _get_window_size(self) -> List[int]:
        monitor_size = pygame.display.get_desktop_sizes()[TARGET_MONITOR_NUM - 1]
        window_width = int(min(TARGET_WINDOW_WIDTH, monitor_size[0] * 9 / 10 ))
        return [window_width, int(window_width / TARGET_ASPECT_RATIO[0] * TARGET_ASPECT_RATIO[1])]

    def run(self):
        self.window = pygame.display.set_mode(self.window_size)
        print(f"Running Graphics App (window size = {self.window_size})")

        draw_properties = self._get_draw_properties(self.window, self.maze)

        while self.running:

            self._event_loop()
            self._ticks = self._clock.tick(TARGET_FPS)

            self._handle_solver_step_calls()

            DrawMaze.draw_maze(self.maze, draw_properties)
            if self.maze_solver: 
                DrawMaze.draw_maze_solution(self.maze_solver, draw_properties)
            self.window.blit(draw_properties.surface, draw_properties.surface_offset)
            
            DrawMaze.draw_steps_per_second(self.window, self._step_calls_per_second)
            DrawMaze.draw_fps_counter(self.window, self._ticks)

            self._late_display_update(draw_properties)


        
        print("Closing Application")
        pygame.quit()

    def _increase_steps(self):
        if self._step_calls_per_second > 2000:
            self._step_calls_per_second += 250
        elif self._step_calls_per_second > 1000:
            self._step_calls_per_second += 100
        elif self._step_calls_per_second > 500:
            self._step_calls_per_second += 50
        elif self._step_calls_per_second > 100:
            self._step_calls_per_second += 25
        elif self._step_calls_per_second > 50:
            self._step_calls_per_second += 10
        elif self._step_calls_per_second > 20:
            self._step_calls_per_second += 5
        elif self._step_calls_per_second > 10:
            self._step_calls_per_second += 2
        else: self._step_calls_per_second += 1

        self._step_calls_per_second = min(5000, self._step_calls_per_second)
        self._step_call_increment = 1000 / self._step_calls_per_second


    def _decrease_steps(self):
        if self._step_calls_per_second > 2000:
            self._step_calls_per_second -= 250
        elif self._step_calls_per_second > 1000:
            self._step_calls_per_second -= 100
        elif self._step_calls_per_second > 500:
            self._step_calls_per_second -= 50
        elif self._step_calls_per_second > 100:
            self._step_calls_per_second -= 25
        elif self._step_calls_per_second > 50:
            self._step_calls_per_second -= 10
        elif self._step_calls_per_second > 20:
            self._step_calls_per_second -= 5
        elif self._step_calls_per_second > 10:
            self._step_calls_per_second -= 2
        else: self._step_calls_per_second -= 1

        self._step_calls_per_second = max(1, self._step_calls_per_second)
        self._step_call_increment = 1000 / self._step_calls_per_second


    def _handle_solver_step_calls(self):
        if not self._run_steps: return
        if not self.maze_solver: return
        if self.maze_solver.solved: return

        self._step_call_counter = min(1000 * self._step_call_increment, self._step_call_counter + self._ticks)
        self._step_call_counter = min(250, self._step_call_counter)
        while self._step_call_counter > self._step_call_increment:
            self.maze_solver.step()
            self._step_call_counter -= self._step_call_increment

    def _manual_step_increment(self):
        if not self.maze_solver: return
        if self.maze_solver.solved: return
        self.maze_solver.step()
    

    def _reset_solver(self):
        if not self.maze_solver: return
        self.maze_solver.setup_data_structures()

    def _event_loop(self):
        self._reset_keys()
        self._events = pygame.event.get()


        for event in self._events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._enable_key(event.dict["key"])


            if event.type == pygame.TEXTINPUT:
                if event.dict["text"] == "s":
                    self._manual_step_increment()
                elif event.dict["text"] == "=":
                    self._increase_steps()
                elif event.dict["text"] == "-":
                    self._decrease_steps()
                

            

    def _reset_keys(self):
        self.k_space = False
        self.k_s = False
        self.k_r = False
        self.k_plus = False
        self.k_minus = False


    def _enable_key(self, key_code: int):
        if key_code == pygame.K_SPACE:
            self.k_space = True
            self._run_steps = not self._run_steps
        elif key_code == pygame.K_s:
            self.k_s = True
        elif key_code == pygame.K_r:
            self.k_r = True
            self._reset_solver()              
        elif key_code == pygame.K_EQUALS:
            self.k_plus = True 
            self._increase_steps()          
        elif key_code == pygame.K_MINUS:
            self.k_minus = True
            self._decrease_steps()


class DrawMaze:
    @classmethod
    def draw_fps_counter(cls, window: pygame.Surface, ticks: int):
        fps = int(1000 / max(1, ticks))
        fps_surface = FPS_FONT.render(f"FPS: {fps} ({int(ticks)}ms)", True, FPS_COUNTER_COLOUR, [200, 200, 200])
        window.blit(fps_surface, [window.get_width() - 180, FPS_COUNTER_SIZE])
    
    @classmethod
    def draw_steps_per_second(cls, window: pygame.Surface, steps: int):
        step_surface = FPS_FONT.render(f"Target Steps per Second: {steps}", True, STEP_COLOUR, [200, 200, 200])
        window.blit(step_surface, [window.get_width() - 240, STEP_SIZE * 2.5])
    
    @classmethod
    def draw_maze(cls, maze: Maze, draw_properties: DrawProperties):

        for node in maze.maze_body:
            if node.walls & TOP_WALL: 
                cls._draw_top_wall(draw_properties.surface, node.x, node.y, draw_properties.wall_width, draw_properties.tile_size)
            if node.walls & BOTTOM_WALL : 
                cls._draw_bottom_wall(draw_properties.surface, node.x, node.y, draw_properties.wall_width, draw_properties.tile_size)
            if node.walls & LEFT_WALL: 
                cls._draw_left_wall(draw_properties.surface, node.x, node.y, draw_properties.wall_width, draw_properties.tile_size)
            if node.walls & RIGHT_WALL: 
                cls._draw_right_wall(draw_properties.surface, node.x, node.y, draw_properties.wall_width, draw_properties.tile_size)   
        
        cls._draw_end(draw_properties.surface, ENTRANCE_TILE_COLOUR, maze.entrance_node.x - 1, maze.entrance_node.y,
                           draw_properties.wall_width, draw_properties.tile_size)
        cls._draw_end(draw_properties.surface, EXIT_TILE_COLOUR, maze.exit_node.x - 1, maze.exit_node.y,
                           draw_properties.wall_width, draw_properties.tile_size)
    
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
            pygame.draw.circle(draw_properties.surface, SOLUTION_TILE_COLOUR, position, solution_circle_size)


    @staticmethod
    def _draw_top_wall(window: pygame.Surface, x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size + wall_width, window.get_height() - ((y + 1) * tile_size) - wall_width]
        wall_dimensions = [tile_size - wall_width, wall_width]

        pygame.draw.rect(window, WALL_COLOUR, [*position, *wall_dimensions])

    @staticmethod
    def _draw_bottom_wall(window: pygame.Surface, x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size + wall_width, window.get_height() - (y * tile_size) - wall_width]
        wall_dimensions = [tile_size - wall_width, wall_width]

        pygame.draw.rect(window, WALL_COLOUR, [*position, *wall_dimensions])
    
    @staticmethod
    def _draw_left_wall(window: pygame.Surface, x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size, window.get_height() - ((y + 1) * tile_size)]
        wall_dimensions = [wall_width, tile_size - wall_width]

        pygame.draw.rect(window, WALL_COLOUR, [*position, *wall_dimensions])

    @staticmethod
    def _draw_right_wall(window: pygame.Surface, x: int, y: int, wall_width: int,
     tile_size: int):
        position = [x * tile_size + tile_size, window.get_height() - (y + 1) * tile_size]
        wall_dimensions = [wall_width, tile_size - wall_width]

        pygame.draw.rect(window, WALL_COLOUR, [*position, *wall_dimensions])


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
