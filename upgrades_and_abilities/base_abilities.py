from typing import final

import pygame
from pygame import Rect, Surface

from config import FPS, HEIGHT


class BaseAbility:
    icon_image: Surface
    base_cooldown: float
    base_mana_cost: int
    name: str

    def __init__(self, screen: Surface, pos_x: int, pos_y: int) -> None:
        self.rect = Rect(pos_x, pos_y, HEIGHT * 0.1, HEIGHT * 0.1)
        self.screen = screen

        self.cooldown = self.base_cooldown
        self.mana_cost = self.base_mana_cost
        self._cooldown_left = 0

    def draw(self) -> None:
        image = pygame.transform.scale(self.icon_image, (self.rect.width, self.rect.height))
        rect = image.get_rect()
        rect.center = self.rect.center
        self.screen.blit(image, rect)

    def process_next_frame(self):
        if self._cooldown_left > 0:
            self._cooldown_left -= 1

    @final
    def use(self, player) -> None:
        if self._cooldown_left == 0:
            self._use(player)
            self._cooldown_left = int(self.cooldown * FPS)

    def _use(self, player) -> None:
        pass
