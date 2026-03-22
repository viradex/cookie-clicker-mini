import math
import constants


class GameManager:
    def __init__(self):
        self.cookies = 0
        self.upgrades = []

    def set_upgrades(self, upgrades: list):
        self.upgrades = upgrades

    def click(self):
        self.cookies += math.floor(self.get_click_power())

    def get_click_power(self) -> int:
        return (
            sum(
                upgrade.total_effect()
                for upgrade in self.upgrades
                if upgrade.upgrade_type == "click"
            )
            + 1
        )

    def get_total_cps(self) -> int:
        return sum(
            upgrade.total_effect()
            for upgrade in self.upgrades
            if upgrade.upgrade_type == "cps"
        )

    def tick(self):
        self.cookies += math.floor(
            self.get_total_cps() / (1000 / constants.UI_UPDATE_FREQUENCY)
        )

    def buy_upgrade(self, upgrade_id: int) -> bool:
        upgrade = self.get_upgrade(upgrade_id)
        if not upgrade:
            return False

        cost = upgrade.get_cost()

        if self.cookies >= cost:
            self.cookies -= cost
            upgrade.amount += 1
            return True

        return False

    def get_upgrade(self, id: int):
        for upgrade in self.upgrades:
            if upgrade.id == id:
                return upgrade

        return None
