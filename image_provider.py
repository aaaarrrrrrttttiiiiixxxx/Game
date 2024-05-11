import pygame
from pygame import Surface


class ImageProvider:
    loaded_images = {}

    @classmethod
    def get_image_by_path(cls, path: str) -> Surface:
        if path not in cls.loaded_images:
            cls.loaded_images[path] = pygame.image.load(path)
        return cls.loaded_images[path]
