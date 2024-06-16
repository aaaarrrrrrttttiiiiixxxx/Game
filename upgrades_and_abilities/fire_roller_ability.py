from pygame import Surface
from pygame.sprite import Group, spritecollide

from camera import Camera
from image_provider import ImageProvider
from units.moving_to_point import MovingToPointUnit
from upgrades_and_abilities.base_abilities import BaseAbility
from upgrades_and_abilities.upgrades import BaseAbilityUpgrade


class FireRoller(MovingToPointUnit):
    image_path = 'resources/units/roller'
    move_speed = 5

    def __init__(self, camera: Camera, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0, damage: int = 0) -> None:
        super().__init__(camera, unit_layer, screen, initial_x, initial_y)
        self.damaged_units = Group()  # type: Group
        self.damage = damage

    def _on_reach_target(self) -> None:
        self.kill()

    def process_next_frame(self):
        super().process_next_frame()
        units = self.unit_layer.units
        units.remove(self.unit_layer.player)
        collided = spritecollide(self, units, False)
        for unit in collided:
            if unit not in self.damaged_units:
                self.damaged_units.add(unit)
                unit.got_attack(self.damage)

        units.add(self.unit_layer.player)


class FireRollerAbility(BaseAbility):
    icon_image = ImageProvider.get_image_by_path('resources/icons/ability_icons/fire_roller.png')
    name = 'Fire roller'
    base_cooldown = 3.0
    base_mana_cost = 10

    def __init__(self, camera: Camera, screen: Surface, pos_x: int, pos_y: int) -> None:
        super().__init__(camera, screen, pos_x, pos_y)
        self.damage = 15

    def _use(self, player) -> None:
        find_target_pos = self.camera.get_mouse()
        fireball = FireRoller(self.camera, player.unit_layer, player.screen, player.rect.centerx, player.rect.centery,
                              self.damage)
        fireball.set_target(*find_target_pos)
        player.unit_layer.add_non_collide(fireball)


class FireRollerDamageUpgrade(BaseAbilityUpgrade):
    ability = FireRollerAbility
    text = '+10 damage'

    def upgrade(self, player) -> None:
        instance = self._get_ability_instance(player)
        if instance is not None:
            instance.damage += 10  # type: ignore


class FireRollerCooldownUpgrade(BaseAbilityUpgrade):
    ability = FireRollerAbility
    text = '-1 cooldown'

    def upgrade(self, player) -> None:
        instance = self._get_ability_instance(player)
        if instance is not None:
            instance.cooldown -= 1

    @classmethod
    def is_available(cls, player) -> bool:
        instance = cls._get_ability_instance(player)
        return instance is not None and instance.cooldown > 1
