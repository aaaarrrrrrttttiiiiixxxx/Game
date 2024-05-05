import contextlib
import logging
import math

import pygame
from pygame import Surface
from pygame.sprite import Sprite

import unit_layer
from config import FONT, RED, FPS, GREEN

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BaseUnit(Sprite):
    image_path = None
    max_hp = None
    base_hp_regen = 0

    def __init__(self, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0):
        super(BaseUnit, self).__init__()
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rect.center = (initial_x, initial_y)
        self.hp = self.max_hp
        self.hp_regen = self.base_hp_regen
        self.screen = screen
        self.unit_layer = unit_layer

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

    def draw_text(self) -> None:
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

    @property
    def radius(self) -> int:
        return int(math.sqrt(self.rect.w ** 2 + self.rect.h ** 2) / 2)


class Player(BaseUnit):
    image_path = "resources/units/player.png"
    max_hp = 1000000


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
        direction_x = self.target.rect.center[0] - self.rect.center[0]
        direction_y = self.target.rect.center[1] - self.rect.center[1]
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
        self.rect.center = (self.rect.center[0] + diff_x, self.rect.center[1] + diff_y)


class BaseMissile(MovingToTargetUnit):
    image_path = None
    move_speed = None
    rotate = False

    def __init__(self, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0, damage: int = 0):
        super().__init__(unit_layer, screen, initial_x, initial_y)
        self.damage = damage

    def on_reach_target(self) -> None:
        self.rect.center = self.target.rect.center
        self.image = pygame.image.load("resources/units/explosion.png")
        super().draw()
        self.kill()
        self.target.got_attack(self.damage)

    def draw(self) -> None:
        self.make_movement_step()
        if self.rotate:
            direction_x = self.target.rect.center[0] - self.rect.center[0]
            direction_y = self.target.rect.center[1] - self.rect.center[1]
            angle = math.degrees(math.atan2(direction_x, direction_y)) - 90

            rotated_image = pygame.transform.rotate(self.image, angle)
            rect_for_draw = rotated_image.get_rect()
            rect_for_draw.center = self.rect.center
            self.screen.blit(rotated_image, rect_for_draw)
            self.draw_text()
        else:
            super().draw()


class Fireball(BaseMissile):
    image_path = "resources/units/fireball.png"
    move_speed = 120 / FPS
    rotate = True


class Arrow(BaseMissile):
    image_path = "resources/units/arrow.png"
    move_speed = 240 / FPS
    rotate = True


class BaseEnemy(MovingToTargetUnit):
    image_path = None
    max_hp = None
    move_speed = None
    damage = None
    attack_range = None
    spawn_rate = 0

    def reach_target(self, distance_x: int, distance_y: int) -> bool:
        attack_range = self.attack_range or self.radius + self.unit_layer.player.radius  # calc melee attack range
        return math.sqrt(distance_x ** 2 + distance_y ** 2) < attack_range

    def on_reach_target(self) -> None:
        self.target.got_attack(self.damage)

    def draw(self) -> None:
        if self.target is not None:
            self.make_movement_step(True)
        super().draw()


class Goblin(BaseEnemy):
    image_path = "resources/units/goblin_64.png"
    max_hp = 50
    move_speed = 60 / FPS
    damage = 1
    attack_range = None
    spawn_rate = 20


class GoblinArcher(BaseEnemy):
    image_path = "resources/units/goblin_archer.png"
    max_hp = 25
    move_speed = 30 / FPS
    damage = 1
    attack_range = 250
    spawn_rate = 10

    def on_reach_target(self) -> None:
        arrow = Arrow(self.unit_layer, self.screen, self.rect.center[0], self.rect.center[1], 1)
        arrow.set_target(self.unit_layer.player)
        self.unit_layer.add_non_collide(arrow)
