from pygame import Surface
from pygame.sprite import Group, spritecollide

from units import BaseUnit, Player, Goblin


class UnitLayer:
    def __init__(self) -> None:
        super().__init__()
        self.units = Group()
        self.non_collide = Group()
        self.player = None

    def add(self, sprite: BaseUnit) -> None:
        self.units.add(sprite)

    def add_non_collide(self, sprite: BaseUnit) -> None:
        self.non_collide.add(sprite)

    def create_player(self, initial_x: int = 0, initial_y: int = 0) -> Player:
        self.player = Player(initial_x, initial_y)
        self.units.add(self.player)
        return self.player

    def create_goblin(self, initial_x: int = 0, initial_y: int = 0) -> Goblin:
        goblin = Goblin(initial_x, initial_y)
        self.units.add(goblin)
        return goblin

    def draw(self, screen: Surface) -> None:
        for unit in self.units:
            unit.draw(screen)
        for unit in self.non_collide:
            unit.draw(screen)

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

    def get_nearest_mob(self, x: int, y: int) -> BaseUnit:
        self.units.remove(self.player)
        res = sorted(self.units, key=lambda s: s.dist_from(x, y))[0]
        self.add(self.player)
        return res
