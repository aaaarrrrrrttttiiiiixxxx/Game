import math
import random
from typing import Type, List

from config import FPS
from unit_layer import UnitLayer
from units.enemies import BaseEnemy


class UnitGenerator:
    SPAWN_RANGE = 300

    def __init__(self, unit_layer: UnitLayer) -> None:
        self.unit_layer = unit_layer
        self.counter = 0

    def step(self) -> None:
        self.counter += 1
        if self.counter % FPS == 0:
            self._step()

    def _step(self) -> None:
        for enemy_type in self._get_all_enemy_types():
            if random.choices([True, False], weights=[enemy_type.get_spawn_rate(), 100])[0]:
                enemy = enemy_type(self.unit_layer, self.unit_layer.screen, *self.get_random_position())
                self.unit_layer.add_enemy(enemy)

    @staticmethod
    def _get_all_enemy_types() -> List[Type[BaseEnemy]]:
        return BaseEnemy.__subclasses__()

    def get_random_position(self) -> tuple[int, int]:
        angle = random.randint(0, 360)
        x, y = self.unit_layer.player.rect.center
        x += int(math.cos(angle) * self.SPAWN_RANGE)
        y += int(math.sin(angle) * self.SPAWN_RANGE)
        return x, y
