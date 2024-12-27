import math
from typing import Union, Optional

import pygame
from pygame import Surface

from EventAggregator import AttackEvent, DealDamageEvent
from camera import Camera
from config import FPS
from units.base_units import MovingToTargetUnit
from units.missiles import Arrow
from upgrades_and_abilities.enemies_abilities.double_damage_hit_ability import DoubleDamageHitAbility


class BaseEnemy(MovingToTargetUnit):
    image_path: str
    move_speed: Union[int, float]
    attack_range: Optional[int]
    lvl1_damage: int
    lvl1_max_hp: int
    lvl1_spawn_rate: int = 0
    lvl1_exp: int = 0

    def __init__(self, camera: Camera, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0) -> None:
        self.max_hp: int = type(self).initial_max_hp()
        self.damage = type(self).initial_damage()
        self.exp = type(self).initial_exp()
        super().__init__(camera, unit_layer, screen, initial_x, initial_y)

    def reach_target(self, distance_x: int, distance_y: int) -> bool:
        attack_range = self.attack_range or self.radius + self.unit_layer.player.radius  # calc melee attack range
        return math.sqrt(distance_x ** 2 + distance_y ** 2) < attack_range

    def _on_reach_target(self) -> None:
        self.attack()

    def _attack(self) -> None:
        if self.target:
            self.event_aggregator.event(AttackEvent(attacking_unit=self, target_unit=self.target, damage=self.damage))
            self.event_aggregator.event(DealDamageEvent(attacking_unit=self, target_unit=self.target, damage=self.damage))

    def draw(self) -> None:
        super().draw()

    def process_next_frame(self) -> None:
        super().process_next_frame()
        if self.target is not None:
            self.make_movement_step(True)

    def _dead(self) -> None:
        super()._dead()
        self.unit_layer.player.add_exp(self.exp)

    @classmethod
    def initial_damage(cls) -> int:
        return cls._upgrade_by_time(cls.lvl1_damage, 0.1)

    @classmethod
    def initial_exp(cls) -> int:
        return cls._upgrade_by_time(cls.lvl1_exp, 0.1)

    @classmethod
    def initial_max_hp(cls) -> int:
        return cls._upgrade_by_time(cls.lvl1_max_hp, 0.1, 5)

    @classmethod
    def get_spawn_rate(cls) -> int:
        return cls._upgrade_by_time(cls.lvl1_spawn_rate, 0.1)

    @staticmethod
    def _upgrade_by_time(value: int, ratio: float, round_factor: int = 1) -> int:
        res = value + ratio * value * pygame.time.get_ticks() / 1000 / 60
        return round_factor * round(int(res) / round_factor)


class Goblin(BaseEnemy):
    image_path = "resources/units/goblin_64.png"
    move_speed = 60 / FPS
    attack_range = None
    attack_speed = 0.5
    lvl1_damage = 5
    lvl1_max_hp = 50
    lvl1_spawn_rate = 20
    lvl1_exp = 35


class GoblinArcher(BaseEnemy):
    image_path = "resources/units/goblin_archer.png"
    move_speed = 30 / FPS
    attack_range = 250
    attack_speed = 0.33
    lvl1_damage = 10
    lvl1_max_hp = 25
    lvl1_spawn_rate = 10
    lvl1_exp = 65

    def _attack(self) -> None:
        self.event_aggregator.event(AttackEvent(attacking_unit=self, target_unit=self.unit_layer.player, damage=self.damage))
        arrow = Arrow(self.camera, self.unit_layer, self.screen, self, self.rect.centerx, self.rect.centery, 1)
        arrow.set_target(self.unit_layer.player)
        self.unit_layer.add_non_collide(arrow)


class BigGoblin(BaseEnemy):
    image_path = "resources/units/dd_goblin.png"
    move_speed = 60 / FPS
    attack_range = None
    attack_speed = 0.5
    lvl1_damage = 10
    lvl1_max_hp = 100
    lvl1_spawn_rate = 5
    lvl1_exp = 70

    def __init__(self, camera: Camera, unit_layer, screen: Surface, initial_x: int = 0, initial_y: int = 0) -> None:
        super().__init__(camera, unit_layer, screen, initial_x, initial_y)
        self.abilities.append(DoubleDamageHitAbility())

    def _on_reach_target(self) -> None:
        ability = self.ability_by_name(DoubleDamageHitAbility.name)
        if ability.is_available(self):  # type: ignore
            ability.use(self)  # type: ignore
        else:
            self.attack()