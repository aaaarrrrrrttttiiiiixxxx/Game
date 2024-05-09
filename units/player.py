import pygame
from pygame import Surface

from config import HIT_NEAREST, LVL_UP, WIDTH, GREEN, HEIGHT
from units.base_units import BaseUnit
from units.missiles import Fireball


class Player(BaseUnit):
    image_path = "resources/units/player.png"
    max_hp = 100
    base_hp_regen = 0.5
    damage = 10
    attack_speed = 1

    def __init__(self, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0) -> None:
        super().__init__(unit_layer, screen, initial_x, initial_y)
        self.level = 1
        self.exp = 0

    def _attack(self) -> None:
        find_target_pos = self.rect.center if HIT_NEAREST else pygame.mouse.get_pos()
        mob = self.unit_layer.get_nearest_mob(*find_target_pos)
        if mob is not None:
            fireball = Fireball(self.unit_layer, self.screen, self.rect.centerx, self.rect.centery, self.damage)
            fireball.set_target(mob)
            self.unit_layer.add_non_collide(fireball)

    def add_exp(self, exp: int) -> None:
        self.exp += exp
        exp_need = self._calc_exp_for_lvl()
        if self.exp >= exp_need:
            self.exp -= exp_need
            self.level += 1
            pygame.event.post(pygame.event.Event(LVL_UP))

    def _calc_exp_for_lvl(self) -> int:
        return self.level * 100 + (self.level - 1) ** 2 * 10

    def draw_exp_line(self) -> None:
        line_len = self.exp / self._calc_exp_for_lvl() * WIDTH
        pygame.draw.line(self.screen, GREEN, (0, HEIGHT - 5), (line_len, HEIGHT - 5), 5)

    def draw(self) -> None:
        super().draw()
        self.draw_exp_line()
