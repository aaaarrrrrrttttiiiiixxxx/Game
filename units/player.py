import pygame

from config import HIT_NEAREST
from units.base_units import BaseUnit
from units.missiles import Fireball


class Player(BaseUnit):
    image_path = "resources/units/player.png"
    max_hp = 100
    base_hp_regen = 0.5
    damage = 10
    attack_speed = 1

    def _attack(self):
        fireball = Fireball(self.unit_layer, self.screen, self.rect.centerx, self.rect.centery, self.damage)
        find_target_pos = self.rect.center if HIT_NEAREST else pygame.mouse.get_pos()
        fireball.set_target(self.unit_layer.get_nearest_mob(*find_target_pos))
        self.unit_layer.add_non_collide(fireball)
