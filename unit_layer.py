import logging

from pygame import Surface
from pygame.sprite import Group, spritecollide

from config import CAMERA_MOVE, WIDTH, HEIGHT
from units import BaseUnit, Player, Goblin, GoblinArcher

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class UnitLayer:
    def __init__(self, screen: Surface) -> None:
        super().__init__()
        self.units = Group()
        self.non_collide = Group()
        self.all_sprites = Group()
        self.player = None
        self.screen = screen

    def add(self, sprite: BaseUnit) -> None:
        self.units.add(sprite)
        self.all_sprites.add(sprite)

    def add_non_collide(self, sprite: BaseUnit) -> None:
        self.non_collide.add(sprite)
        self.all_sprites.add(sprite)

    def create_player(self, initial_x: int = None, initial_y: int = None) -> Player:
        self.player = Player(self, self.screen, initial_x or WIDTH / 2, initial_y or HEIGHT / 2)
        self.units.add(self.player)
        self.all_sprites.add(self.player)
        return self.player

    def create_goblin(self, initial_x: int = 0, initial_y: int = 0) -> Goblin:
        goblin = Goblin(self, self.screen, initial_x, initial_y)
        goblin.set_target(self.player)
        self.units.add(goblin)
        self.all_sprites.add(goblin)
        return goblin

    def create_goblin_archer(self, initial_x: int = 0, initial_y: int = 0) -> Goblin:
        goblin = GoblinArcher(self, self.screen, initial_x, initial_y)
        goblin.set_target(self.player)
        self.units.add(goblin)
        self.all_sprites.add(goblin)
        return goblin

    def draw(self) -> None:
        for unit in self.units:
            unit.draw()
        for unit in self.non_collide:
            unit.draw()

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
        if (CAMERA_MOVE is None or
                self.player.rect.left < WIDTH * CAMERA_MOVE or
                self.player.rect.right > WIDTH * (1 - CAMERA_MOVE) or
                self.player.rect.top < HEIGHT * CAMERA_MOVE or
                self.player.rect.bottom > HEIGHT * (1 - CAMERA_MOVE)):
            self.all_sprites.update('move', diff_x=-diff_x, diff_y=-diff_y)

    def get_nearest_mob(self, x: int, y: int) -> BaseUnit:
        self.units.remove(self.player)
        res = sorted(self.units, key=lambda s: s.dist_from(x, y))[0]
        self.add(self.player)
        return res
