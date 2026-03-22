import json
import math
from pathlib import Path

import constants
from models.upgrade import Upgrade


class SaveManager:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.data_dir = self.base_dir / "data"
        self.json_path = self.data_dir / "save.json"

        self.data = self._load()

    def _make_readonly(self):
        if constants.MAKE_SAVE_FILE_READONLY:
            self.json_path.chmod(0o444)

    def _make_writeable(self):
        self.json_path.chmod(0o644)

    def _default_data(self):
        return {
            "cookies": 0,
            "upgrades": [
                {"id": uid, "amount": 0}
                for uid in constants.UPGRADES_DEFAULT_DATA.keys()
            ],
        }

    def _load(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

        try:
            with self.json_path.open("r") as file:
                content = file.read().strip()
                if not content:
                    self.data = self._default_data()
                    self.save()

                    return self.data

                return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            self.data = self._default_data()
            self.save()

            return self.data

    def save(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

        if self.json_path.exists():
            self._make_writeable()

        with self.json_path.open("w") as file:
            json.dump(self.data, file, indent=2)

        self._make_readonly()

    def get_cookies(self):
        return self.data["cookies"]

    def get_upgrades(self):
        upgrades = []

        for saved in self.data["upgrades"]:
            uid = saved["id"]
            amount = saved["amount"]

            definition = constants.UPGRADES_DEFAULT_DATA[uid]

            upgrades.append(
                Upgrade(
                    id=uid,
                    name=definition["name"],
                    base_cost=definition["base_cost"],
                    effect=definition["effect"],
                    upgrade_type=definition["upgrade_type"],
                    amount=amount,
                )
            )

        return upgrades

    def add_cookies(self, amount):
        self.data["cookies"] += amount

    def spend_cookies(self, amount):
        if self.data["cookies"] >= amount:
            self.data["cookies"] -= amount
            return True

        return False

    def add_upgrade(self, upgrade_id):
        for upgrade in self.data["upgrades"]:
            if upgrade["id"] == upgrade_id:
                upgrade["amount"] += 1
                return

    def reset(self):
        self._make_writeable()

        self.data = self._default_data()
        self.save()

        self._make_readonly()

    def lock_file(self):
        self._make_readonly()
