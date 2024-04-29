import pygame
from pygame import Surface
from pygame.sprite import Sprite


class BaseUnit(Sprite):
    image_path = None

    def __init__(self, initial_x: int = 0, initial_y: int = 0):
        super(BaseUnit, self).__init__()
        self.image = pygame.image.load(self.image_path)
        self.rect = self.image.get_rect()
        self.rect.x += initial_x
        self.rect.y += initial_y

    def move(self, diff_x: int, diff_y: int) -> None:
        self.rect.x += diff_x
        self.rect.y += diff_y

    def draw(self, screen: Surface) -> None:
        screen.blit(self.image, self.rect)


class Player(BaseUnit):
    image_path = "resources/units/player.png"


class Fireball(BaseUnit):
    image_path = "resources/units/fireball.png"


class Goblin(BaseUnit):
    image_path = "resources/units/goblin_64.png"
