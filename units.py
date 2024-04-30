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

    def __init__(self, screen: Surface, initial_x: int = 0, initial_y: int = 0):
        super(BaseUnit, self).__init__()
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (initial_x, initial_y)
        self.hp = self.max_hp
        self.hp_regen = self.base_hp_regen
        self.screen = screen

    def move(self, diff_x: int, diff_y: int) -> None:
        self.rect.x += diff_x
        self.rect.y += diff_y

    def dist_from(self, x: int, y: int) -> float:
        return math.sqrt((self.rect.x - x) * (self.rect.x - x) + (self.rect.y - y) * (self.rect.y - y))

    def draw(self) -> None:
        self.screen.blit(self.image, self.rect)
        if self.max_hp:
            img2 = FONT.render(f'{self.hp} / {self.max_hp}', True, RED)
            x, y = self.rect.topleft
            y -= 10
            self.screen.blit(img2, (x, y))

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


class MovingToTargetUnit(BaseUnit):
    move_speed = None

    def __init__(self, screen: Surface, initial_x: int = 0, initial_y: int = 0):
        super().__init__(screen, initial_x, initial_y)
        self.target = None
        self.real_x = float(initial_x)
        self.real_y = float(initial_y)
        self.rect.center = int(self.real_x), int(self.real_y)

    def set_target(self, target: BaseUnit) -> None:
        self.target = target

    def on_reach_target(self) -> None:
        pass

    def make_movement_step(self) -> None:
        direction_x = self.target.rect.center[0] - self.real_x
        direction_y = self.target.rect.center[1] - self.real_y
        if abs(direction_x) + abs(direction_y) < self.move_speed:
            self.rect.center = self.target.rect.center
            self.on_reach_target()
            return
        if direction_y == 0:
            move_x = self.move_speed
            move_y = 0
        else:
            ratio = abs(direction_x / direction_y)
            move_y = self.move_speed / math.sqrt(ratio * ratio + 1)
            move_x = move_y * ratio
        self.real_x += move_x if direction_x > 0 else -move_x
        self.real_y += move_y if direction_y > 0 else -move_y
        self.rect.center = int(self.real_x), int(self.real_y)

    def move(self, diff_x: int, diff_y: int) -> None:
        self.rect.x += diff_x
        self.rect.y += diff_y
        self.real_x += float(diff_x)
        self.real_y += float(diff_y)


class Fireball(MovingToTargetUnit):
    image_path = "resources/units/fireball.png"
    move_speed = 120 / FPS

    def __init__(self, screen: Surface, initial_x: int = 0, initial_y: int = 0, damage: int = 0):
        super().__init__(screen, initial_x, initial_y)
        self.damage = damage

    def on_reach_target(self) -> None:
        self.image = pygame.image.load("resources/units/explosion.png")
        super().draw()
        self.kill()
        self.target.got_attack(self.damage)

    def draw(self) -> None:
        self.make_movement_step()
        super().draw()


class Goblin(BaseUnit):
    image_path = "resources/units/goblin_64.png"
    max_hp = 50
