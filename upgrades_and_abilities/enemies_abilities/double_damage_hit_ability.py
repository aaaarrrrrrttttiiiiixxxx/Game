from upgrades_and_abilities.base_abilities import BaseAbility


class DoubleDamageHitAbility(BaseAbility):
    base_cooldown = 10.0
    base_mana_cost = 0
    name = "Double Damage Hit"

    def _use(self, ability_owner) -> None:
        ability_owner.damage *= 2
        ability_owner.attack()
        ability_owner.damage /= 2
