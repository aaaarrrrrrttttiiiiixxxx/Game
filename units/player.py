import contextlib
import logging
from typing import List, Union, Tuple

import pygame
from pygame import Surface

from EventAggregator import AttackEvent, DealDamageEvent
from camera import Camera
from config import LVL_UP, WIDTH, HEIGHT, CAMERA_MOVE, RED, UPGRADE_FONT, BLUE, WHITE, FPS
from units.base_units import BaseUnit
from units.image_stores import ImageStore, BaseImageStore, EmptyStoreException
from upgrades_and_abilities.base_abilities import PlayerAbility

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class PlayerDeadException(Exception):
    pass


class PlayerImageStore(BaseImageStore):

    def __init__(self, path: str, reloaded: bool = True) -> None:
        self.stores: List[Union[BaseImageStore, ImageStore]] = [ImageStore(path + "attack"),
                                                                ImageStore(path + "run"),
                                                                BaseImageStore(path + 'base.png')]

    def next_frame(self) -> None:
        for store in self.stores:
            store.next_frame()

    def get_image(self) -> Surface:  # type: ignore
        for store in self.stores:
            with contextlib.suppress(EmptyStoreException):
                return store.get_image()

    def change_direction(self, is_left: bool) -> None:
        if self.stores[1].is_end() or is_left != self.stores[1].is_left:
            self.stores[1].reload(is_left)

    def attack(self, is_left: bool) -> None:
        self.stores[0].reload(is_left)


class Player(BaseUnit):
    image_path = "resources/units/player/"
    max_hp = 10
    base_hp_regen = 0.5
    damage = 25
    attack_speed = 1
    image_store_type = PlayerImageStore

    def __init__(self, camera: Camera, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0) -> None:
        super().__init__(camera, unit_layer, screen, initial_x, initial_y)
        self.level = 1
        self.exp = 0
        self.max_mp = 50
        self.mp_regen = 0.5
        self.mp = 50.0

        self.abilities: List[PlayerAbility] = []  # type: ignore

    def _attack(self) -> None:  # melee
        mob = self.unit_layer.get_nearest_mob(*self.rect.center)
        if mob is not None and mob.dist_from(*self.rect.center) < 130:
            self.event_aggregator.event(AttackEvent(attacking_unit=self, target_unit=mob, damage=self.damage))
            self.event_aggregator.event(DealDamageEvent(attacking_unit=self, target_unit=mob, damage=self.damage))
            self.image_store.attack((mob.rect.centerx - self.rect.centerx) < 0)

    def add_exp(self, exp: int) -> None:
        self.exp += exp
        exp_need = self._calc_exp_for_lvl()
        if self.exp >= exp_need:
            self.exp -= exp_need
            self.level += 1
            pygame.event.post(pygame.event.Event(LVL_UP))

    def _calc_exp_for_lvl(self) -> int:
        return self.level * 100 + (self.level - 1) ** 2 * 10

    def draw_bottom_bar(self) -> None:

        text = UPGRADE_FONT.render(f'LVL {self.level}', True, WHITE)
        self.screen.blit(text, (0, HEIGHT - text.get_rect().height - 40))

        text = UPGRADE_FONT.render(f'{int(self.mp)} / {self.max_mp}', True, BLUE)
        self.screen.blit(text, (0, HEIGHT - text.get_rect().height - 20))

        text = UPGRADE_FONT.render(f'{int(self.hp)} / {self.max_hp}', True, RED)
        self.screen.blit(text, (0, HEIGHT - text.get_rect().height - 0))

        self.draw_bottom_line(self.exp, self._calc_exp_for_lvl(), WHITE, 40)
        self.draw_bottom_line(self.mp, self.max_mp, BLUE, 20)
        self.draw_bottom_line(self.hp, self.max_hp, RED, 0)

    def draw_bottom_line(self, line_val: Union[int, float], line_max: Union[int, float],
                         color: Tuple[int, int, int], padding: int) -> None:
        left_pad = 120
        height = 20

        line_len = line_val / line_max * (WIDTH - left_pad)
        if line_len:
            y = HEIGHT - 0.5 * height - padding
            pygame.draw.line(self.screen, color, (left_pad, y), (left_pad + line_len, y), height)

    def draw_interface(self) -> None:
        super().draw_interface()
        self.draw_bottom_bar()
        self.draw_abilities()

    def draw_abilities(self) -> None:
        for ability in self.abilities:
            ability.draw()

    def move(self, diff_x: Union[int, float], diff_y: Union[int, float], screen: bool = False) -> None:
        super().move(diff_x, diff_y)
        logger.debug(f"move {diff_x} {diff_y}")
        if (diff_x != 0 or diff_y != 0) and not screen:
            self.image_store.change_direction(diff_x < 0)  # type: ignore

        if (CAMERA_MOVE is None or
                self.rect.left - self.camera.x < WIDTH * CAMERA_MOVE or
                self.rect.right - self.camera.x > WIDTH * (1 - CAMERA_MOVE) or
                self.rect.top - self.camera.y < HEIGHT * CAMERA_MOVE or
                self.rect.bottom - self.camera.y > HEIGHT * (1 - CAMERA_MOVE)):
            self.camera.x += int(diff_x)
            self.camera.y += int(diff_y)

    def process_next_frame(self) -> None:
        super().process_next_frame()

        self.mp += self.mp_regen / FPS
        if self.mp > self.max_mp:
            self.mp = self.max_mp

        for ability in self.abilities:
            ability.process_next_frame()

    def use_ability(self, ind: int) -> None:
        self.abilities[ind].use(self)

    def _dead(self) -> None:
        raise PlayerDeadException
