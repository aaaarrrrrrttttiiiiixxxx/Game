from typing import final

import pygame
from pygame import Rect, Surface

from config import FPS, HEIGHT, HIT_NEAREST
from image_provider import ImageProvider
from units.missiles import Fireball


class BaseAbility:
    icon_image: Surface
    base_cooldown: float
    base_mana_cost: int
    name: str

    def __init__(self, screen: Surface, pos_x: int, pos_y: int) -> None:
        self.rect = Rect(pos_x, pos_y, HEIGHT * 0.1, HEIGHT * 0.1)
        self.screen = screen

        self._cooldown = self.base_cooldown
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
            self._cooldown_left = int(self._cooldown * FPS)

    def _use(self, player) -> None:
        pass


class FireballAbility(BaseAbility):
    icon_image = ImageProvider.get_image_by_path('resources/icons/ability_icons/fireball.png')
    name = 'Fireball'
    base_cooldown = 3.0
    base_mana_cost = 10

    def __init__(self, screen: Surface, pos_x: int, pos_y: int) -> None:
        super().__init__(screen, pos_x, pos_y)
        self.damage = 35

    def _use(self, player) -> None:
        print(1)
        find_target_pos = player.rect.center if HIT_NEAREST else pygame.mouse.get_pos()
        mob = player.unit_layer.get_nearest_mob(*find_target_pos)
        if mob is not None:
            fireball = Fireball(player.unit_layer, player.screen, player.rect.centerx, player.rect.centery, self.damage)
            fireball.set_target(mob)
            player.unit_layer.add_non_collide(fireball)
