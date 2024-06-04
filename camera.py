from typing import Union, Tuple

import pygame


class Camera:
    def __init__(self) -> None:
        self.x: int = 0
        self.y: int = 0

    def map(self, x: Union[int, float], y: Union[int, float]) -> tuple[int | float, int | float]:
        return x - self.x, y - self.y

    def get_mouse(self) -> tuple[int | float, int | float]:
        return pygame.mouse.get_pos()[0] + self.x, pygame.mouse.get_pos()[1] + self.y
