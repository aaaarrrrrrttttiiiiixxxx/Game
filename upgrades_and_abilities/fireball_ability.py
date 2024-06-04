import pygame
from pygame import Surface

from camera import Camera
from config import HIT_NEAREST, FPS
from image_provider import ImageProvider
from units.missiles import BaseMissile
from upgrades_and_abilities.base_abilities import BaseAbility
from upgrades_and_abilities.upgrades import BaseAbilityUpgrade


class Fireball(BaseMissile):
    image_path = "resources/units/fireball.png"
    move_speed = 120 / FPS
    rotate = True


class FireballAbility(BaseAbility):
    icon_image = ImageProvider.get_image_by_path('resources/icons/ability_icons/fireball.png')
    name = 'Fireball'
    base_cooldown = 3.0
    base_mana_cost = 10

    def __init__(self, camera: Camera, screen: Surface, pos_x: int, pos_y: int) -> None:
        super().__init__(camera, screen, pos_x, pos_y)
        self.damage = 35

    def _use(self, player) -> None:
        find_target_pos = player.rect.center if HIT_NEAREST else self.camera.get_mouse()
        mob = player.unit_layer.get_nearest_mob(*find_target_pos)
        if mob is not None:
            fireball = Fireball(self.camera, player.unit_layer, player.screen, player.rect.centerx, player.rect.centery, self.damage)
            fireball.set_target(mob)
            player.unit_layer.add_non_collide(fireball)


class FireballDamageUpgrade(BaseAbilityUpgrade):
    ability = FireballAbility
    text = '+20 damage'

    def upgrade(self, player) -> None:
        instance = self._get_ability_instance(player)
        if instance is not None:
            instance.damage += 20  # type: ignore


class FireballCooldownUpgrade(BaseAbilityUpgrade):
    ability = FireballAbility
    text = '-1 cooldown'

    def upgrade(self, player) -> None:
        instance = self._get_ability_instance(player)
        if instance is not None:
            instance.cooldown -= 1

    @classmethod
    def is_available(cls, player) -> bool:
        instance = cls._get_ability_instance(player)
        return instance is not None and instance.cooldown >= 1
