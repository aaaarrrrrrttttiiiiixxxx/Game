import contextlib
import logging
import math
from typing import final

import pygame
from pygame import Surface
from pygame.sprite import Sprite

from config import FONT, RED, FPS

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BaseUnit(Sprite):
    image_path = None
    max_hp = None
    base_hp_regen = 0
    attack_speed = None

    def __init__(self, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0):
        super(BaseUnit, self).__init__()
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rect.width /= 2
        self.rect.height /= 2
        self.rect.center = (initial_x, initial_y)
        self.hp = self.max_hp
        self.hp_regen = self.base_hp_regen
        self.screen = screen
        self.unit_layer = unit_layer
        if self.attack_speed:
            self.attack_freeze = 0

    def move(self, diff_x: int, diff_y: int) -> None:
        self.rect.x += diff_x
        self.rect.y += diff_y

    def move_to(self, res_x: int, res_y: int) -> None:
        self.rect.x = res_x
        self.rect.y = res_y

    def dist_from(self, x: int, y: int) -> float:
        return math.sqrt((self.rect.x - x) * (self.rect.x - x) + (self.rect.y - y) * (self.rect.y - y))

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)
        # pygame.draw.rect(self.screen, RED, self.rect, 2)
        # pygame.draw.circle(self.screen, GREEN, self.rect.center, self.radius, 2)
        self.draw_text()

    def attack(self):
        if self.attack_speed and self.attack_freeze <= 0:
            self._attack()
            self.attack_freeze = FPS / self.attack_speed

    def _attack(self):
        pass

    def draw_text(self) -> None:
        if self.max_hp and self.hp:
            img2 = FONT.render(f'{int(self.hp)} / {self.max_hp}', True, RED)
            x, y = self.rect.topleft
            y -= 10
            self.screen.blit(img2, (x, y))

    def got_attack(self, damage: int) -> None:
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def process_next_frame(self):
        if self.max_hp and self.hp and self.hp_regen:
            self.hp += self.hp_regen / FPS
            if self.hp > self.max_hp:
                self.hp = self.max_hp
        if self.attack_speed:
            self.attack_freeze -= 1

    @final
    def update(self, action: str, **kwargs) -> None:
        with contextlib.suppress(AttributeError, TypeError):
            self.__getattribute__(action)(**kwargs)

    @property
    def radius(self) -> int:
        return int(math.sqrt(self.rect.w ** 2 + self.rect.h ** 2) / 2)


class MovingToTargetUnit(BaseUnit):
    move_speed = None

    def __init__(self, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0):
        super().__init__(unit_layer, screen, initial_x, initial_y)
        self.target = None
        self.rect.center = initial_x, initial_y

    def set_target(self, target: BaseUnit) -> None:
        self.target = target

    def on_reach_target(self) -> None:
        pass

    def reach_target(self, distance_x: int, distance_y: int) -> bool:
        return math.sqrt(distance_x ** 2 + distance_y ** 2) < self.move_speed

    def make_movement_step(self, use_collide: bool = False) -> None:
        direction_x = self.target.rect.centerx - self.rect.centerx
        direction_y = self.target.rect.centery - self.rect.centery
        if self.reach_target(direction_x, direction_y):
            self.on_reach_target()
            return
        if direction_y == 0:
            move_x = self.move_speed
            move_y = 0
        else:
            ratio = abs(direction_x / direction_y)
            move_y = self.move_speed / math.sqrt(ratio * ratio + 1)
            move_x = move_y * ratio
        diff_x = move_x if direction_x > 0 else -move_x
        diff_y = move_y if direction_y > 0 else -move_y
        if use_collide:
            self.unit_layer.move(self, 0, diff_y)
            self.unit_layer.move(self, diff_x, 0)
        else:
            self.move(diff_x, diff_y)

    def move(self, diff_x: int, diff_y: int) -> None:
        self.rect.center = (self.rect.centerx + diff_x, self.rect.centery + diff_y)
