import tkinter as tk

from ui.main_screen import MainScreen
from logic.game_manager import GameManager


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Cookie Clicker Mini")
        self.geometry("800x550")
        self.minsize(650, 500)

        self.game_manager = GameManager()

        self.ui = MainScreen(self, self.game_manager)

    def run(self):
        self.mainloop()
