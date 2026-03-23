import tkinter as tk
from tkinter import messagebox
import math
import random
import sys
import os

import constants
from ui.main_screen import MainScreen
from logic.game_manager import GameManager
from logic.save_manager import SaveManager
from logic.number import abbreviate_number


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cookie Clicker Mini")
        self.iconbitmap("assets/app.ico")
        self.geometry("800x550")
        self.minsize(650, 500)

        self.game_manager = GameManager()
        self.save_manager = SaveManager()
        self.upgrades = self.save_manager.get_upgrades()

        self.check_if_save_tampered()
        self.setup()

    def setup(self):
        self.load_game()

        self.ui = MainScreen(self, self.game_manager, self.upgrades)
        self.game_manager.set_upgrades(self.upgrades)

        self.schedule_frenzy()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def save_game_state(self):
        self.save_manager.data["cookies"] = self.game_manager.cookies

        for upgrade in self.upgrades:
            for saved in self.save_manager.data["upgrades"]:
                if saved["id"] == upgrade.id:
                    saved["amount"] = upgrade.amount
                    saved["discovered"] = upgrade.discovered

    def check_if_save_tampered(self):
        is_readonly = self.save_manager.is_readonly()
        if not is_readonly:
            messagebox.showwarning(
                "Save File Warning",
                "The save file has been detected to be writeable and may have been tampered with. Due to this, data from the last save may be missing or corrupt.\n\nIf the program crashes, delete the save file and restart.",
            )

    def start_loops(self):
        self.ui_loop()
        self.game_loop()
        self.title_loop()
        self.save_loop()

    def ui_loop(self):
        self.ui.update_ui()
        self.after(constants.UI_UPDATE_FREQUENCY, self.ui_loop)

    def game_loop(self):
        frenzy_ended = self.game_manager.tick()
        unlocked_ids = self.game_manager.check_unlocks()

        if frenzy_ended:
            self.ui.change_cookie_img(gold=False)
        if unlocked_ids:
            self.on_upgrades_unlocked(unlocked_ids)

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

    def schedule_frenzy(self):
        delay = random.randint(constants.FRENZY_DELAY_MIN, constants.FRENZY_DELAY_MAX)
        self.after(delay, self.spawn_frenzy)

    def spawn_frenzy(self):
        self.ui.show_frenzy_button()
        self.frenzy_timeout = self.after(constants.FRENZY_MISS_DELAY, self.miss_frenzy)

    def miss_frenzy(self):
        self.ui.hide_frenzy_button()
        self.schedule_frenzy()

    def on_upgrades_unlocked(self, upgrades_ids):
        for uid in upgrades_ids:
            for saved in self.save_manager.data["upgrades"]:
                if saved["id"] == uid:
                    saved["discovered"] = True

    def on_frenzy_clicked(self):
        # Cancel miss timeout
        if hasattr(self, "frenzy_timeout"):
            self.after_cancel(self.frenzy_timeout)

        # Wait for frenz to end then spawn again
        duration = self.game_manager.frenzy_time_left
        self.after(duration, self.schedule_frenzy)

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
