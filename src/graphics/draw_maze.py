from typing import List

import pygame

from src.base_maze import Maze, MazeNode

TARGET_ASPECT_RATIO = [16, 9]
TARGET_WINDOW_WIDTH = 1280
TARGET_FPS = 60
TARGET_MONITOR_NUM = 1

WALL_COLOUR = [32, 200, 32]

pygame.init()



class GraphicsApp:
    def __init__(self) -> None:
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
            self._clock.tick(TARGET_FPS)
            pygame.draw.rect(self.window, WALL_COLOUR, [100, 200, 10, 200])
            self.event_loop()
            pygame.display.update()

    
    def event_loop(self):
        self._events = pygame.event.get()
        for event in self._events:
            if event.type == pygame.QUIT:
                self.running = False
    
