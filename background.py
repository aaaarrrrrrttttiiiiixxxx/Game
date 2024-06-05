import pygame
from pygame import Surface

from camera import Camera
from config import WIDTH, HEIGHT
from image_provider import ImageProvider


class Background:

    def __init__(self, camera: Camera, screen: Surface) -> None:
        self.camera = camera
        self.screen = screen
        self.height = 300
        self.width = 300
        self.background = ImageProvider.get_image_by_path('resources/background/grass300.jpg')
        self.background = pygame.transform.scale(self.background, (self.height, self.width))

    def draw(self) -> None:
        for x in range(self.camera.x // self.width, 1 + (self.camera.x + WIDTH) // self.width):
            for y in range(self.camera.y // self.height, 1 + (self.camera.y + HEIGHT) // self.height):
                self.screen.blit(self.background, self.camera.map(x * self.width, y * self.height))
