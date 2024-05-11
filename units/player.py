import contextlib
import logging
import os
from typing import List, Optional

import pygame
from pygame import Surface

from config import HIT_NEAREST, LVL_UP, WIDTH, GREEN, HEIGHT
from image_provider import ImageProvider
from units.base_units import BaseUnit
from units.missiles import Fireball

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ImageStore:
    def __init__(self, path: str) -> None:
        self.images = [f'{path}/{i}' for i in os.listdir(path)]
        self.ind = len(self.images)
        self._is_left = False

    def next_frame(self) -> None:
        self.ind += 0.5

    def reload(self, is_left: bool) -> None:
        self.ind = 0
        self._is_left = is_left

    def get_image(self) -> Optional[Surface]:
        with contextlib.suppress(IndexError):
            return pygame.transform.flip(ImageProvider.get_image_by_path(self.images[int(self.ind)]), self._is_left, False)


class BaseImageStore:
    def __init__(self, path: str) -> None:
        self.img_path = path
        self._is_left = False
        pass

    def next_frame(self) -> None:
        pass

    def reload(self, is_left: bool) -> None:
        self._is_left = is_left

    def get_image(self) -> Optional[Surface]:
        return pygame.transform.flip(ImageProvider.get_image_by_path(self.img_path), self._is_left, False)


class PlayerImageProvider:

    def __init__(self):
        self.stores = [ImageStore("resources/units/player/attack"),
                       ImageStore("resources/units/player/run"),
                       BaseImageStore('resources/units/player/base.png')]

    def next_frame(self):
        for store in self.stores:
            store.next_frame()

    def get_current_image(self) -> Surface:
        for store in self.stores:
            image = store.get_image()
            if image is not None:
                return image

    def change_direction(self, is_left: bool):
        self.stores[1].reload(is_left)

    def attack(self, is_left: bool):
        self.stores[0].reload(is_left)


class Player(BaseUnit):
    image_path = "resources/units/player/attack/attack_01.png"
    max_hp = 100
    base_hp_regen = 0.5
    damage = 10
    attack_speed = 1

    def __init__(self, unit_layer, image_provider: PlayerImageProvider, screen: Surface, initial_x: int = 0,
                 initial_y: int = 0) -> None:
        super().__init__(unit_layer, screen, initial_x, initial_y)
        self.image_provider = image_provider
        self.level = 1
        self.exp = 0

    # def _attack(self) -> None: # fireball
    #     find_target_pos = self.rect.center if HIT_NEAREST else pygame.mouse.get_pos()
    #     mob = self.unit_layer.get_nearest_mob(*find_target_pos)
    #     if mob is not None:
    #         fireball = Fireball(self.unit_layer, self.screen, self.rect.centerx, self.rect.centery, self.damage)
    #         fireball.set_target(mob)
    #         self.unit_layer.add_non_collide(fireball)

    def _attack(self) -> None:  # melee
        mob = self.unit_layer.get_nearest_mob(*self.rect.center)
        if mob is not None and mob.dist_from(*self.rect.center) < 130:
            mob.got_attack(self.damage)
            self.image_provider.attack((mob.rect.centerx - self.rect.centerx) < 0)

    def add_exp(self, exp: int) -> None:
        self.exp += exp
        exp_need = self._calc_exp_for_lvl()
        if self.exp >= exp_need:
            self.exp -= exp_need
            self.level += 1
            pygame.event.post(pygame.event.Event(LVL_UP))

    def _calc_exp_for_lvl(self) -> int:
        return self.level * 100 + (self.level - 1) ** 2 * 10

    def draw_exp_line(self) -> None:
        line_len = self.exp / self._calc_exp_for_lvl() * WIDTH
        pygame.draw.line(self.screen, GREEN, (0, HEIGHT - 5), (line_len, HEIGHT - 5), 5)

    def draw(self) -> None:
        self.image = self.image_provider.get_current_image()
        super().draw()
        self.draw_exp_line()

    def move(self, diff_x: int, diff_y: int, screen: bool = False) -> None:
        super().move(diff_x, diff_y)
        logger.debug(f"move {diff_x} {diff_y}")
        if diff_x != 0 and not screen:
            self.image_provider.change_direction(diff_x < 0)
