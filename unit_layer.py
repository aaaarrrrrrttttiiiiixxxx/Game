from pygame import Surface
from pygame.sprite import Group, spritecollide

from player import BaseUnit


class UnitLayer:
    def __init__(self) -> None:
        super().__init__()
        self.units = Group()

    def add(self, sprite: BaseUnit) -> None:
        self.units.add(sprite)

    def draw(self, screen: Surface) -> None:
        for unit in self.units:
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
