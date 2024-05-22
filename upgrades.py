from typing import Tuple, List

from pygame import Surface

from abilities import BaseAbility
from image_provider import ImageProvider
from units import player
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


class UpgradeFactory:

    def __init__(self) -> None:
        self._init_ability_upgrades()

    def get_all_upgrades(self) -> List[BaseUpgrade]:
        res = []
        for upgrade_class in BaseUpgrade.__subclasses__():
            res.append(upgrade_class())
        return res

    def _init_ability_upgrades(self):
        for ability_class in BaseAbility.__subclasses__():
            ability_upgrade_class = type(f"{ability_class.name}Upgrade", (BaseUpgrade,), dict())
            setattr(ability_upgrade_class, 'text', ability_class.name)
            setattr(ability_upgrade_class, 'image', ability_class.icon_image)

            def upgrade(self, player: Player) -> None:
                try:
                    pos_x = player.abilities[-1].rect.right
                except IndexError:
                    pos_x = 0
                player.abilities.append(ability_class(player.screen, pos_x + 5, 5))

            setattr(ability_upgrade_class, 'upgrade', upgrade)
