import math

from config import FPS
from units.base_units import MovingToTargetUnit
from units.missiles import Arrow


class BaseEnemy(MovingToTargetUnit):
    image_path = None
    max_hp = None
    move_speed = None
    damage = None
    attack_range = None
    spawn_rate = 0

    def reach_target(self, distance_x: int, distance_y: int) -> bool:
        attack_range = self.attack_range or self.radius + self.unit_layer.player.radius  # calc melee attack range
        return math.sqrt(distance_x ** 2 + distance_y ** 2) < attack_range

    def on_reach_target(self) -> None:
        self.attack()

    def _attack(self):
        self.target.got_attack(self.damage)
        print(f'{id(self)} {self.damage}')

    def draw(self) -> None:
        super().draw()

    def process_next_frame(self):
        super().process_next_frame()
        if self.target is not None:
            self.make_movement_step(True)


class Goblin(BaseEnemy):
    image_path = "resources/units/goblin_64.png"
    max_hp = 50
    move_speed = 60 / FPS
    damage = 3
    attack_range = None
    spawn_rate = 20
    attack_speed = 0.5


class GoblinArcher(BaseEnemy):
    image_path = "resources/units/goblin_archer.png"
    max_hp = 25
    move_speed = 30 / FPS
    damage = 6
    attack_range = 250
    spawn_rate = 10
    attack_speed = 0.33

    def _attack(self):
        arrow = Arrow(self.unit_layer, self.screen, self.rect.centerx, self.rect.centery, 1)
        arrow.set_target(self.unit_layer.player)
        self.unit_layer.add_non_collide(arrow)
        print(f'{id(self)} {self.damage}')
