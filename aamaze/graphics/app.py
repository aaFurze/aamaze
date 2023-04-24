import os
from typing import List

import pygame

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

pygame.init()

from aamaze.base_maze import Maze, SolvingAlgorithm
from aamaze.graphics.defaults import (DEFAULT_BACKGROUND_COLOUR,
                                      DEFAULT_ENTRANCE_TILE_COLOUR,
                                      DEFAULT_EXIT_TILE_COLOUR,
                                      DEFAULT_SHOW_FPS_COUNTER,
                                      DEFAULT_SHOW_STEPS_COUNTER,
                                      DEFAULT_SOLUTION_TILE_COLOUR,
                                      DEFAULT_START_PAUSED,
                                      DEFAULT_TARGET_ASPECT_RATIO,
                                      DEFAULT_TARGET_FPS,
                                      DEFAULT_TARGET_MONITOR_NUM,
                                      DEFAULT_TARGET_STEPS_PER_SECOND,
                                      DEFAULT_TARGET_WINDOW_WIDTH,
                                      DEFAULT_WALL_COLOUR)
from aamaze.graphics.draw_maze import DrawMaze, DrawProperties


class GraphicsApp:
    def __init__(self, maze: Maze, maze_solver: SolvingAlgorithm = None) -> None:
        self.maze = maze
        self.maze_solver = maze_solver

        self._options = GraphicsAppOptionsConfigurer()
        self._generation_manipulator = MazeGenerationManipulator(self.maze_solver)

        self.window: pygame.Surface

        self.running = True
    
        self._clock = pygame.time.Clock()
        self._ticks: int = 0
        self._events = List[pygame.event.Event]

        self.k_space: bool
        self.k_s: bool
        self.k_r: bool
        self.k_plus: bool
        self.k_minus: bool

        self._reset_keys()


    @property
    def option_list(self):
        return list(self._options.__dict__.keys())


    def configure(self, **kwargs):
        for key in kwargs.keys():
            setattr(self._options, key, kwargs[key])


    def _get_draw_properties(self, window: pygame.Surface, maze: Maze) -> DrawProperties:
        output = DrawProperties()
        output.configure_properties(window, maze, self._options.entrance_colour, self._options.exit_colour,
                                     self._options.solution_colour, self._options.wall_colour)
        return output
    
    def _late_display_update(self, draw_properties: DrawProperties):
        pygame.display.update()
        self.window.fill(self._options.background_colour)
        draw_properties.surface.fill(self._options.background_colour)

    def _get_window_size(self) -> List[int]:
        monitor_size = pygame.display.get_desktop_sizes()[DEFAULT_TARGET_MONITOR_NUM - 1]
        window_width = int(min(self._options.window_width, monitor_size[0] * 9 / 10 ))
        return [window_width, int(window_width / self._options.aspect_ratio[0] * self._options.aspect_ratio[1])]

    def run(self):
        pygame.display.set_caption("aamaze")
        self.window = pygame.display.set_mode(self._get_window_size())
        print(f"Running Graphics App (window size = {self.window.get_size()})")

        draw_properties = self._get_draw_properties(self.window, self.maze)

        self._generation_manipulator.run_steps = not self._options.start_paused
        self._generation_manipulator.set_steps_per_second(self._options.target_steps_per_second)

        while self.running:

            self._event_loop()
            self._ticks = self._clock.tick(self._options.target_fps)

            self._generation_manipulator.handle_solver_step_calls(self._ticks)

            DrawMaze.draw_maze(self.maze, draw_properties)
            if self.maze_solver: 
                DrawMaze.draw_maze_solution(self.maze_solver, draw_properties)
            self.window.blit(draw_properties.surface, draw_properties.surface_offset)
            

            if self._options.show_fps_counter: DrawMaze.draw_fps_counter(self.window, self._ticks)
            if self._options.show_step_counter: DrawMaze.draw_steps_per_second(self.window, self._generation_manipulator._step_calls_per_second)

            self._late_display_update(draw_properties)

        print("Closing Application")
        pygame.quit()

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
                    self._generation_manipulator.manual_step_increment()
                elif event.dict["text"] == "=":
                    self._generation_manipulator.increase_steps()
                elif event.dict["text"] == "-":
                    self._generation_manipulator.decrease_steps()
                
    def _reset_keys(self):
        self.k_space = False
        self.k_s = False
        self.k_r = False
        self.k_plus = False
        self.k_minus = False

    def _enable_key(self, key_code: int):
        if key_code == pygame.K_SPACE:
            self.k_space = True
            self._generation_manipulator.run_steps = not self._generation_manipulator.run_steps
        elif key_code == pygame.K_s:
            self.k_s = True
        elif key_code == pygame.K_r:
            self.k_r = True
            self._generation_manipulator.reset_solver()              
        elif key_code == pygame.K_EQUALS:
            self.k_plus = True        
        elif key_code == pygame.K_MINUS:
            self.k_minus = True



class GraphicsAppOptionsConfigurer:
    def __init__(self) -> None:
        self.aspect_ratio = DEFAULT_TARGET_ASPECT_RATIO
        self.background_colour = DEFAULT_BACKGROUND_COLOUR
        self.entrance_colour = DEFAULT_ENTRANCE_TILE_COLOUR
        self.exit_colour = DEFAULT_EXIT_TILE_COLOUR
        self.show_fps_counter = DEFAULT_SHOW_FPS_COUNTER
        self.show_step_counter = DEFAULT_SHOW_STEPS_COUNTER
        self.solution_colour = DEFAULT_SOLUTION_TILE_COLOUR
        self.start_paused = DEFAULT_START_PAUSED
        self.target_fps = DEFAULT_TARGET_FPS
        self.target_steps_per_second = DEFAULT_TARGET_STEPS_PER_SECOND
        self.wall_colour = DEFAULT_WALL_COLOUR
        self.window_width = DEFAULT_TARGET_WINDOW_WIDTH



class MazeGenerationManipulator:
    _increment_bounds = {2000: 250, 1000: 100, 500: 50, 100: 25, 50: 10, 20: 5, 10: 2, 1: 1}

    def __init__(self, maze_solver: SolvingAlgorithm) -> None:
        self.maze_solver = maze_solver

        self._step_calls_per_second = 50
        self._step_call_increment = 1000 / self._step_calls_per_second
        self._step_call_counter = 0
        self.run_steps = True

    def decrease_steps(self):

        for bound_increment in self._increment_bounds.items():
            if self._step_calls_per_second > bound_increment[0]:
                self._step_calls_per_second -= bound_increment[1]
                break

        self.set_steps_per_second(self._step_calls_per_second)

    def handle_solver_step_calls(self, ticks: int):
        if not self.run_steps: return
        if not self.maze_solver: return
        if self.maze_solver.solved: return

        self._step_call_counter = min(1001, self._step_call_counter + ticks)

        while self._step_call_counter > self._step_call_increment:
            self.maze_solver.step()
            self._step_call_counter -= self._step_call_increment

    def increase_steps(self):

        for bound_increment in self._increment_bounds.items():
            if self._step_calls_per_second >= bound_increment[0]:
                self._step_calls_per_second += bound_increment[1]
                break

        self.set_steps_per_second(self._step_calls_per_second)

    def manual_step_increment(self):
        if not self.maze_solver: return
        if self.maze_solver.solved: return
        self.maze_solver.step()
    
    def reset_solver(self):
        if not self.maze_solver: return
        self.maze_solver.setup_data_structures()
    
    def set_steps_per_second(self, value):
        self._step_calls_per_second = max(1, min(5000, value))

        for bound_increment in self._increment_bounds.items():
            if self._step_calls_per_second >= bound_increment[0]:
                self._round_steps_per_second(bound_increment[1])
                break

        self._step_call_increment = 1000 / self._step_calls_per_second

    def _round_steps_per_second(self, round_to: int):
        self._step_calls_per_second = int(self._step_calls_per_second / round_to) * round_to
