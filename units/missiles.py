import math

import pygame
from pygame import Surface

from config import FPS
from units.base_units import MovingToTargetUnit


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
        if self.rotate:
            direction_x = self.target.rect.centerx - self.rect.centerx
            direction_y = self.target.rect.centery - self.rect.centery
            angle = math.degrees(math.atan2(direction_x, direction_y)) - 90

            rotated_image = pygame.transform.rotate(self.image, angle)
            rect_for_draw = rotated_image.get_rect()
            rect_for_draw.center = self.rect.center
            self.screen.blit(rotated_image, rect_for_draw)
            self.draw_text()
        else:
            super().draw()

    def process_next_frame(self):
        super().process_next_frame()
        self.make_movement_step()


class Fireball(BaseMissile):
    image_path = "resources/units/fireball.png"
    move_speed = 120 / FPS
    rotate = True


class Arrow(BaseMissile):
    image_path = "resources/units/arrow.png"
    move_speed = 240 / FPS
    rotate = True
