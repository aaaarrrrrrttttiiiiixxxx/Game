from typing import Callable, List, Tuple, Optional

import pygame
from pygame import Surface
from pygame.event import Event

from config import WIDTH, HEIGHT, RED, UPGRADE_FONT
from image_provider import ImageProvider
from upgrades_and_abilities.upgrades import BaseUpgrade


class AbilityChooseScreen:

    def __init__(self, screen: Surface, upgrade_list: List[BaseUpgrade]) -> None:
        self.upgrade_list = upgrade_list
        self.screen = screen
        self.buttons: List[UpgradeButton] = []
        self.init_buttons_row(2)

        self.result: Optional[BaseUpgrade] = None

    def draw(self) -> None:
        for button in self.buttons:
            button.draw()

    def init_buttons_row(self, padding_ratio: int) -> None:
        count_x = len(self.upgrade_list)
        padding_x = WIDTH // (count_x + 1 + count_x * padding_ratio)
        size_x = padding_x * padding_ratio
        padding_y = HEIGHT // 4
        size_y = padding_y * 2
        for x in range(count_x):
            self.buttons.append(
                UpgradeButton(self.screen, (padding_x + size_x) * x + padding_x, padding_y,
                              size_x, size_y, self.upgrade_list[x], callback=self._callback, result=x))

    def _callback(self, result: int) -> None:
        self.result = self.upgrade_list[result]

    def handle_event(self, event: Event) -> None:
        for button in self.buttons:
            button.handle_event(event)


class UpgradeButton:
    background_image = ImageProvider.get_image_by_path("resources/menu/ability_choose.png")

    def __init__(self, screen: Surface, pos_x: int, pos_y: int, width: int, height: int, upgrade: BaseUpgrade,
                 callback: Callable, **kwargs) -> None:
        self.rect = pygame.Rect(pos_x, pos_y, width, height)
        self.screen = screen
        self.text, self.icon_image = upgrade.get_drawable()
        self.callback = callback
        self.kwargs = kwargs

    def draw(self) -> None:
        image = pygame.transform.scale(self.background_image, (self.rect.width, self.rect.height))
        rect = image.get_rect()
        rect.center = self.rect.center
        self.screen.blit(image, rect)

        icon = self._resize_image(self.icon_image)
        image_rect = icon.get_rect()
        image_rect.center = self._get_icon_position()
        self.screen.blit(icon, image_rect)

        img2 = UPGRADE_FONT.render(self.text, True, RED)
        text_rect = img2.get_rect()
        text_rect.center = self._get_text_position()
        self.screen.blit(img2, text_rect)

    def _resize_image(self, icon: Surface) -> Surface:
        return pygame.transform.scale(icon, (HEIGHT // 4.5, HEIGHT // 4.5))

    def _get_icon_position(self) -> Tuple[int, int]:
        return self.rect.centerx, int(self.rect.y + self.rect.height / 5 * 2)

    def _get_text_position(self) -> Tuple[int, int]:
        return self.rect.centerx, int(self.rect.y + self.rect.height / 4 * 3)

    def is_hover(self) -> bool:
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def handle_event(self, event: Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hover():
            self.callback(**self.kwargs)
