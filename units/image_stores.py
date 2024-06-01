import os

import pygame
from pygame import Surface

from image_provider import ImageProvider


class EmptyStoreException(Exception):
    ...


class BaseImageStore:
    def __init__(self, path: str, reloaded: bool = True) -> None:
        if os.path.isdir(path):
            self.images = [f'{path}/{i}' for i in os.listdir(path)]
        else:
            self.images = [path]
        self.ind = 0 if reloaded else float(len(self.images))

        self._is_left = False

    def next_frame(self) -> None:
        pass

    def attack(self, is_left: bool) -> None:
        pass

    def reload(self, is_left: bool) -> None:
        self.ind = 0
        self._is_left = is_left

    def get_image(self) -> Surface:
        return pygame.transform.flip(ImageProvider.get_image_by_path(self.get_image_path()), self._is_left, False)

    def get_image_path(self) -> str:
        if self.ind >= len(self.images):
            self.on_animation_end()
        return self.images[int(self.ind)]

    def on_animation_end(self):
        self.ind = 0


class ImageStore(BaseImageStore):

    def next_frame(self) -> None:
        self.ind += 0.5

    def on_animation_end(self):
        raise EmptyStoreException


class InfinityImageStore(ImageStore):

    def on_animation_end(self):
        self.ind = 0
