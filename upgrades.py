from typing import Tuple

from pygame import Surface

from image_provider import ImageProvider
from units.player import Player


class BaseUpgrade:
    text: str
    image: Surface

    def get_drawable(self) -> Tuple[str, Surface]:
        return self.text, self.image

    def upgrade(self, player: Player) -> None:
        pass


class HPUpgrade(BaseUpgrade):
    text: str = '+ 25 HP'
    image: Surface = ImageProvider.get_image_by_path("resources/icons/128/HeartFull.png")

    def upgrade(self, player: Player) -> None:
        player.max_hp += 25
        player.hp += 25


class HPRagenUpgrade(BaseUpgrade):
    text: str = '+ 1 HP regen'
    image: Surface = ImageProvider.get_image_by_path("resources/icons/128/PotionRed.png")

    def upgrade(self, player: Player) -> None:
        player.hp_regen += 1


class DamageUpgrade(BaseUpgrade):
    text: str = '+ 5 damage'
    image: Surface = ImageProvider.get_image_by_path("resources/icons/128/SwordT2.png")

    def upgrade(self, player: Player) -> None:
        player.damage += 5
