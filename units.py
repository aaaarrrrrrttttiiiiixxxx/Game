import contextlib
import logging
import math

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

    def __init__(self, initial_x: int = 0, initial_y: int = 0):
        super(BaseUnit, self).__init__()
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (initial_x, initial_y)
        self.hp = self.max_hp
        self.hp_regen = self.base_hp_regen

    def move(self, diff_x: int, diff_y: int) -> None:
        self.rect.x += diff_x
        self.rect.y += diff_y

    def dist_from(self, x: int, y: int) -> float:
        return math.sqrt((self.rect.x - x) * (self.rect.x - x) + (self.rect.y - y) * (self.rect.y - y))

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)
        if self.max_hp:
            img2 = FONT.render(f'{self.hp} / {self.max_hp}', True, RED)
            x, y = self.rect.topleft
            y -= 10
            screen.blit(img2, (x, y))

    def got_attack(self, damage: int) -> None:
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def update(self, action: str, **kwargs) -> None:
        with contextlib.suppress(AttributeError, TypeError):
            self.__getattribute__(action)(**kwargs)


class Player(BaseUnit):
    image_path = "resources/units/player.png"
    max_hp = 100


class Fireball(BaseUnit):
    image_path = "resources/units/fireball.png"
    move_speed = 120 / FPS

    def __init__(self, unit_from: BaseUnit, unit_to: BaseUnit, damage: int) -> None:
        super().__init__(unit_from.rect.center[0], unit_from.rect.center[1])
        self.unit_to = unit_to
        self.real_x = float(unit_from.rect.center[0])
        self.real_y = float(unit_from.rect.center[1])
        self.rect.center = int(self.real_x), int(self.real_y)

        self.damage = damage

    def draw(self, screen: Surface) -> None:
        direction_x = self.unit_to.rect.center[0] - self.real_x
        direction_y = self.unit_to.rect.center[1] - self.real_y
        if abs(direction_x) + abs(direction_y) < self.move_speed:
            self.image = pygame.image.load("resources/units/explosion.png")
            self.rect.center = self.unit_to.rect.center
            super().draw(screen)
            self.kill()
            self.unit_to.got_attack(self.damage)
            return

        if direction_y == 0:
            move_x = self.move_speed
            move_y = 0
        else:
            ratio = abs(direction_x / direction_y)
            move_y = self.move_speed / math.sqrt(ratio * ratio + 1)
            move_x = move_y * ratio
        logger.debug(f'{move_x}, {move_y}')
        self.real_x += move_x if direction_x > 0 else -move_x
        self.real_y += move_y if direction_y > 0 else -move_y
        self.rect.center = int(self.real_x), int(self.real_y)

        super().draw(screen)

    def move(self, diff_x: int, diff_y: int) -> None:
        self.rect.x += diff_x
        self.rect.y += diff_y
        self.real_x += float(diff_x)
        self.real_y += float(diff_y)

class Goblin(BaseUnit):
    image_path = "resources/units/goblin_64.png"
    max_hp = 50
