import tkinter as tk

import constants
from ui.main_screen import MainScreen
from logic.game_manager import GameManager
from models.upgrade import Upgrade


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cookie Clicker Mini")
        self.iconbitmap("assets/cookie.ico")
        self.geometry("800x550")
        self.minsize(650, 500)

        self.game_manager = GameManager()
        self.upgrades = []

        self.setup()

    def setup(self):
        self.create_upgrades()
        self.ui = MainScreen(self, self.game_manager, self.upgrades)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_loops(self):
        self.ui_loop()
        self.game_loop()
        self.save_loop()

    def ui_loop(self):
        self.ui.update_ui()
        self.after(100, self.ui_loop)

    def game_loop(self):
        # self.game_manager.tick()
        self.after(100, self.game_loop)

    def save_loop(self):
        # self.save_manager.save()
        self.after(10000, self.save_loop)

    def on_close(self):
        # self.save_manager.save()
        self.destroy()

    def load_game(self):
        # self.save_manager.load()
        pass

    def create_upgrades(self):
        upgrades_data = [
            ("Cursor", constants.CURSOR_BASE_COST, constants.CURSOR_EFFECT, "click"),
            ("Worker", constants.WORKER_BASE_COST, constants.WORKER_EFFECT, "cps"),
            ("Farm", constants.FARM_BASE_COST, constants.FARM_EFFECT, "cps"),
            ("Factory", constants.FACTORY_BASE_COST, constants.FACTORY_EFFECT, "cps"),
        ]

        for i, (name, cost, effect, upgrade_type) in enumerate(upgrades_data):
            self.upgrades.append(Upgrade(i, name, cost, effect, upgrade_type))

    def run(self):
        self.mainloop()
