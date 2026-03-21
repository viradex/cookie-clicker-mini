import tkinter as tk
from ui.main_screen import MainScreen


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cookie Clicker Mini")
        self.root.geometry("800x550")
        self.root.minsize(650, 500)

        self.ui = MainScreen(self.root)

    def run(self):
        self.root.mainloop()
