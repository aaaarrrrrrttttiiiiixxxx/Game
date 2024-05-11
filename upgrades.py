import pygame

from image_provider import ImageProvider
from units.player import Player


class BaseUpgrade:
    text = None
    image = None

    def get_drawable(self):
        return self.text, self.image

    def upgrade(self, player: Player):
        pass


class HPUpgrade(BaseUpgrade):
    text = "+ 25 HP"
    image = ImageProvider.get_image_by_path("resources/icons/128/HeartFull.png")

    def upgrade(self, player: Player):
        player.max_hp += 25
        player.hp += 25


class HPRagenUpgrade(BaseUpgrade):
    text = "+ 1 HP regen"
    image = ImageProvider.get_image_by_path("resources/icons/128/PotionRed.png")

    def upgrade(self, player: Player):
        player.hp_regen += 1


class DamageUpgrade(BaseUpgrade):
    text = "+ 5 damage"
    image = ImageProvider.get_image_by_path("resources/icons/128/SwordT2.png")

    def upgrade(self, player: Player):
        player.damage += 5