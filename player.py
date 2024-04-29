import pygame
from pygame import Surface
from pygame.sprite import Sprite


class Player(Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("resources/units/goblin_64.png")
        self.rect = self.image.get_rect()

    def move(self, diff_x: int, diff_y: int):
        self.rect.x += diff_x
        self.rect.y += diff_y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
