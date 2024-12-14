from pygame import Surface

from camera import Camera
from image_provider import ImageProvider
from upgrades_and_abilities.base_abilities import PlayerAbility
from upgrades_and_abilities.upgrades import BaseAbilityUpgrade
from utils import calc_movement_step


class BlinkAbility(PlayerAbility):
    icon_image = ImageProvider.get_image_by_path('resources/icons/ability_icons/blink.png')
    name = 'Blink'
    base_cooldown = 10.0
    base_mana_cost = 10

    def __init__(self, camera: Camera, screen: Surface, pos_x: int, pos_y: int) -> None:
        super().__init__(camera, screen, pos_x, pos_y)
        self._max_dist = 300

    def _use(self, ability_owner) -> None:
        target_pos = self.camera.get_mouse()
        ability_owner.move(*calc_movement_step(*target_pos, *ability_owner.rect.center, self._max_dist))  # type: ignore


class FireRollerCooldownUpgrade(BaseAbilityUpgrade):
    ability = BlinkAbility
    text = '-1 cooldown'

    def upgrade(self, player) -> None:
        instance = self._get_ability_instance(player)
        if instance is not None:
            instance.cooldown -= 1

    @classmethod
    def is_available(cls, player) -> bool:
        instance = cls._get_ability_instance(player)
        return instance is not None and instance.cooldown > 1
