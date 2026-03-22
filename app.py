import tkinter as tk
import math

import constants
from ui.main_screen import MainScreen
from logic.game_manager import GameManager
from logic.save_manager import SaveManager
from logic.number import abbreviate_number
from models.upgrade import Upgrade


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cookie Clicker Mini -- 0 cookies")
        self.iconbitmap("assets/app.ico")
        self.geometry("800x550")
        self.minsize(650, 500)

        self.game_manager = GameManager()
        self.save_manager = SaveManager()
        self.upgrades = self.save_manager.get_upgrades()

        self.setup()

    def setup(self):
        self.load_game()

        self.ui = MainScreen(self, self.game_manager, self.upgrades)
        self.game_manager.set_upgrades(self.upgrades)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def save_game_state(self):
        self.save_manager.data["cookies"] = self.game_manager.cookies

        for upgrade in self.upgrades:
            for saved in self.save_manager.data["upgrades"]:
                if saved["id"] == upgrade.id:
                    saved["amount"] = upgrade.amount

    def start_loops(self):
        self.ui_loop()
        self.game_loop()
        self.title_loop()
        self.save_loop()

    def ui_loop(self):
        self.ui.update_ui()
        self.after(constants.UI_UPDATE_FREQUENCY, self.ui_loop)

    def game_loop(self):
        self.game_manager.tick()
        self.after(constants.UI_UPDATE_FREQUENCY, self.game_loop)

    def title_loop(self):
        self.title(
            f"Cookie Clicker Mini -- {abbreviate_number(math.floor(self.game_manager.cookies))} cookies"
        )
        self.after(constants.TITLE_UPDATE_FREQUENCY, self.title_loop)

    def save_loop(self):
        self.save_game_state()
        self.save_manager.save()
        self.after(constants.SAVE_FREQUENCY, self.save_loop)

    def on_close(self):
        self.save_game_state()
        self.save_manager.save()
        self.save_manager.lock_file()

        self.destroy()

    def load_game(self):
        self.game_manager.cookies = self.save_manager.get_cookies()

    def run(self):
        self.start_loops()
        self.mainloop()
