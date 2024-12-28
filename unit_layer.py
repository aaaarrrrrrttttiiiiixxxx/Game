import logging
from typing import Optional, Type

from pygame import Surface
from pygame.sprite import Group, spritecollide

from camera import Camera
from config import WIDTH
from units.base_units import BaseUnit, BaseDrawable
from units.enemies import Goblin, GoblinArcher, BaseEnemy
from units.player import Player

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UnitLayer:
    def __init__(self, camera: Camera, screen: Surface) -> None:
        self.camera = camera
        self.units = Group()  # type: Group
        self.non_collide = Group()  # type: Group
        self.all_sprites = Group()  # type: Group
        self.screen = screen
        self.player = self._create_player()

    def add(self, sprite: BaseUnit) -> None:
        self.units.add(sprite)
        self.all_sprites.add(sprite)

    def add_non_collide(self, sprite: BaseDrawable) -> None:
        self.non_collide.add(sprite)
        self.all_sprites.add(sprite)

    def _create_player(self) -> Player:
        self.player = Player(self.camera, self, self.screen, int(WIDTH / 2), int(WIDTH / 2))
        self.units.add(self.player)
        self.all_sprites.add(self.player)
        return self.player

    def create_goblin(self, initial_x: int = 0, initial_y: int = 0) -> Goblin:
        goblin = Goblin(self.camera, self, self.screen, initial_x, initial_y)
        self.add_enemy(goblin)
        return goblin

    def create_goblin_archer(self, initial_x: int = 0, initial_y: int = 0) -> GoblinArcher:
        goblin = GoblinArcher(self.camera, self, self.screen, initial_x, initial_y)
        self.add_enemy(goblin)
        return goblin

    def create_enemy(self, enemy_type: Type, initial_x: int = 0, initial_y: int = 0):
        enemy = enemy_type(self.camera, self, self.screen, initial_x, initial_y)
        self.add_enemy(enemy)
        return enemy

    def add_enemy(self, enemy: BaseEnemy) -> None:
        enemy.set_target(self.player)
        self.add(enemy)

    def draw(self) -> None:
        for unit in self.units:
            unit.draw()
        for unit in self.non_collide:
            unit.draw()
        for unit in self.units:
            unit.draw_interface()
        for unit in self.non_collide:
            unit.draw_interface()

    def process_next_frame(self) -> None:
        for unit in self.units:
            unit.process_next_frame()
        for unit in self.non_collide:
            unit.process_next_frame()

    def move(self, sprite: BaseUnit, diff_x: int, diff_y: int) -> None:
        if diff_x != 0 and diff_y != 0:
            raise Exception('Diagonal move is not suppoted')
        self.units.remove(sprite)
        sprite.move(diff_x, diff_y)
        collided = spritecollide(sprite, self.units, False)
        if collided:
            if diff_x > 0:
                most_collided = sorted(collided, key=lambda s: s.rect.x)[0]
                sprite.rect.right = most_collided.rect.left
            elif diff_x < 0:
                most_collided = sorted(collided, key=lambda s: s.rect.x, reverse=True)[0]
                sprite.rect.left = most_collided.rect.right
            elif diff_y > 0:
                most_collided = sorted(collided, key=lambda s: s.rect.y)[0]
                sprite.rect.bottom = most_collided.rect.top
            else:
                most_collided = sorted(collided, key=lambda s: s.rect.y, reverse=True)[0]
                sprite.rect.top = most_collided.rect.bottom

        self.add(sprite)

    def move_player(self, diff_x: int, diff_y: int) -> None:
        self.move(self.player, diff_x, diff_y)

    def get_nearest_mob(self, x: int, y: int) -> Optional[BaseUnit]:
        if len(self.units) <= 1:
            return None
        self.units.remove(self.player)
        res = sorted(self.units, key=lambda s: s.dist_from(x, y))[0]
        self.add(self.player)
        return res
