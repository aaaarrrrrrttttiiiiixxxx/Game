from typing import Tuple, List, Type, Optional

from pygame import Surface

from image_provider import ImageProvider
from upgrades_and_abilities.base_abilities import BaseAbility


class BaseUpgrade:
    text: str
    image: Surface

    def get_drawable(self) -> Tuple[str, Surface]:
        return self.text, self.image

    def upgrade(self, player) -> None:
        pass

    @classmethod
    def is_available(cls, player) -> bool:
        return True


class BaseAbilityUpgrade(BaseUpgrade):
    ability: Type[BaseAbility]

    def get_drawable(self) -> Tuple[str, Surface]:
        return self.text, self.ability.icon_image

    @classmethod
    def is_available(cls, player) -> bool:
        return cls._get_ability_instance(player) is not None

    @classmethod
    def _get_ability_instance(cls, player) -> Optional[BaseAbility]:
        return player.ability_by_name(cls.ability.name)


class HPUpgrade(BaseUpgrade):
    text: str = '+ 25 HP'
    image: Surface = ImageProvider.get_image_by_path("resources/icons/128/HeartFull.png")

    def upgrade(self, player) -> None:
        player.max_hp += 25
        player.hp += 25


class HPRagenUpgrade(BaseUpgrade):
    text: str = '+ 1 HP regen'
    image: Surface = ImageProvider.get_image_by_path("resources/icons/128/PotionRed.png")

    def upgrade(self, player) -> None:
        player.hp_regen += 1


class DamageUpgrade(BaseUpgrade):
    text: str = '+ 5 damage'
    image: Surface = ImageProvider.get_image_by_path("resources/icons/128/SwordT2.png")

    def upgrade(self, player) -> None:
        player.damage += 5


class UpgradeFactory:

    def __init__(self, player) -> None:
        self.player = player
        self._init_ability_upgrades()

    def get_all_upgrades(self) -> List[BaseUpgrade]:
        res = []
        existing_abilities = self.player.ability_names
        for upgrade_class in self.__get_upgrades_classes():
            if upgrade_class.text not in existing_abilities and upgrade_class.is_available(self.player):
                res.append(upgrade_class())
        return res

    def __get_upgrades_classes(self, cls: type = BaseUpgrade) -> List[Type[BaseUpgrade]]:
        res = []
        for child in cls.__subclasses__():
            subclasses = self.__get_upgrades_classes(child)
            if len(subclasses) == 0:
                res.append(child)
            else:
                res.extend(subclasses)
        return res

    def _init_ability_upgrades(self):
        for ability_class in BaseAbility.__subclasses__():
            ability_upgrade_class = type(f"{ability_class.name}Upgrade", (BaseUpgrade,), dict())
            setattr(ability_upgrade_class, 'text', ability_class.name)
            setattr(ability_upgrade_class, 'image', ability_class.icon_image)

            def upgrade(self, player) -> None:
                try:
                    pos_x = player.abilities[-1].rect.right
                except IndexError:
                    pos_x = 0
                player.abilities.append(ability_class(player.screen, pos_x + 5, 5))

            setattr(ability_upgrade_class, 'upgrade', upgrade)
