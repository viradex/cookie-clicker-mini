from dataclasses import dataclass

import constants


@dataclass
class Upgrade:
    id: int
    name: str
    base_cost: int
    effect: int
    upgrade_type: str  # 'click' or 'cps'
    amount: int = 0

    def get_cost(self) -> int:
        return int(self.base_cost * (constants.CPS_MULTIPLIER**self.amount))

    def total_effect(self) -> int:
        return self.amount * self.effect
