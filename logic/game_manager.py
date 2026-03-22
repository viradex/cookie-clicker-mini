import constants


class GameManager:
    def __init__(self):
        self.cookies = 0
        self.upgrades = []

    def set_upgrades(self, upgrades: list):
        self.upgrades = upgrades

    def click(self):
        self.cookies += self.get_click_power()

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
        self.cookies += self.get_total_cps() / (1000 / constants.UI_UPDATE_FREQUENCY)

    def buy_upgrade(self, upgrade_name: str) -> bool:
        upgrade = self.get_upgrade(upgrade_name)
        if not upgrade:
            return False

        cost = upgrade.get_cost()

        if self.cookies >= cost:
            self.cookies -= cost
            upgrade.amount += 1
            return True

        return False

    def get_upgrade(self, name: str):
        for upgrade in self.upgrades:
            if upgrade.name.lower() == name.lower():
                return upgrade

        return None
