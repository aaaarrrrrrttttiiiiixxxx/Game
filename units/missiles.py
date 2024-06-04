import math

import pygame
from pygame import Surface

from camera import Camera
from config import FPS
from units.base_units import MovingToTargetUnit


class BaseMissile(MovingToTargetUnit):
    rotate = False

    def __init__(self, camera: Camera, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0, damage: int = 0) -> None:
        super().__init__(camera, unit_layer, screen, initial_x, initial_y)
        self.damage = damage

    def _on_reach_target(self) -> None:
        if self.target is not None:
            self.rect.center = self.target.rect.center
            super().draw()
            self.kill()
            self.target.got_attack(self.damage)

    def draw(self) -> None:
        if self.rotate and self.target:
            direction_x = self.target.rect.centerx - self.rect.centerx
            direction_y = self.target.rect.centery - self.rect.centery
            angle = math.degrees(math.atan2(direction_x, direction_y)) - 90

            rotated_image = pygame.transform.rotate(self.image_store.get_image(), angle)
            rect_for_draw = rotated_image.get_rect()
            rect_for_draw.center = self.rect.center
            self.screen.blit(rotated_image, self.camera.map(*rect_for_draw.topleft))
            self.draw_text()
        else:
            super().draw()

    def process_next_frame(self) -> None:
        super().process_next_frame()
        self.make_movement_step()


class Arrow(BaseMissile):
    image_path = "resources/units/arrow.png"
    move_speed = 240 / FPS
    rotate = True
