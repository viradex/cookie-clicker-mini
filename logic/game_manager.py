import math
import random
import constants


class GameManager:
    def __init__(self):
        self.cookies = 0
        self._cookie_remainder = 0.0
        self.upgrades = []

        # Frenzy
        self.frenzy_active = False
        self.frenzy_type = None
        self.frenzy_multiplier = 1
        self.frenzy_time_left = 0

    def set_upgrades(self, upgrades: list):
        self.upgrades = upgrades

    def click(self):
        self.cookies += math.floor(self.get_click_power())

    def get_click_power(self) -> int:
        base = (
            sum(
                upgrade.total_effect()
                for upgrade in self.upgrades
                if upgrade.upgrade_type == "click"
            )
            + 1
        )

        if self.frenzy_active and self.frenzy_type == "click":
            base *= self.frenzy_multiplier

        return base

    def get_total_cps(self) -> int:
        base = sum(
            upgrade.total_effect()
            for upgrade in self.upgrades
            if upgrade.upgrade_type == "cps"
        )

        if self.frenzy_active and self.frenzy_type == "cps":
            base *= self.frenzy_multiplier

        return base

    def tick(self):
        frenzy_ended = False

        self._cookie_remainder += self.get_total_cps() / (
            1000 / constants.UI_UPDATE_FREQUENCY
        )
        cookies_to_add = math.floor(self._cookie_remainder)

        self.cookies += cookies_to_add
        self._cookie_remainder -= cookies_to_add

        if self.frenzy_active:
            self.frenzy_time_left -= constants.UI_UPDATE_FREQUENCY

            if self.frenzy_time_left <= 0:
                frenzy_ended = True
                self.frenzy_active = False
                self.frenzy_type = None
                self.frenzy_multiplier = 1

        return frenzy_ended

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

    def start_frenzy(self):
        self.frenzy_active = True
        self.frenzy_type = random.choice(["cps", "click"])

        self.frenzy_multiplier = random.choice(constants.POSSIBLE_FRENZY_MULTIPLIERS)
        self.frenzy_time_left = random.randint(
            constants.FRENZY_DURATION_MIN, constants.FRENZY_DURATION_MAX
        )
