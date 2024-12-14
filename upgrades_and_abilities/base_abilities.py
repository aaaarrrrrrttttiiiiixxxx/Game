from typing import final

import pygame
from pygame import Rect, Surface

from camera import Camera
from config import FPS, HEIGHT


class BaseAbility:
    base_cooldown: float
    base_mana_cost: int
    name: str

    def __init__(self) -> None:
        self.cooldown = self.base_cooldown
        self.mana_cost = self.base_mana_cost
        self._cooldown_left = 0

    def process_next_frame(self):
        if self._cooldown_left > 0:
            self._cooldown_left -= 1

    @final
    def use(self, ability_owner) -> None:
        if self.is_available(ability_owner):
            self._use(ability_owner)
            self._cooldown_left = int(self.cooldown * FPS)
            ability_owner.mp -= self.mana_cost

    def is_available(self, ability_owner) -> bool:
        return self._cooldown_left == 0 and self.mana_cost <= ability_owner.mp

    def _use(self, ability_owner) -> None:
        pass


class PlayerAbility(BaseAbility):
    icon_image: Surface

    def __init__(self, camera: Camera, screen: Surface, pos_x: int, pos_y: int) -> None:
        super().__init__()
        self.rect = Rect(pos_x, pos_y, HEIGHT * 0.1, HEIGHT * 0.1)
        self.screen = screen
        self.camera = camera

    def draw(self) -> None:
        image = pygame.transform.scale(self.icon_image, (self.rect.width, self.rect.height))
        rect = image.get_rect()
        rect.center = self.rect.center
        self.screen.blit(image, rect)
