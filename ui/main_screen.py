import tkinter as tk
from tkinter import ttk

import constants
from logic.number import abbreviate_number
from logic.game_manager import GameManager


class MainScreen:
    def __init__(self, root: tk.Tk, game_manager: GameManager, upgrades: list):
        self.root = root
        self.game_manager = game_manager
        self.upgrades = upgrades
        self.upgrade_widgets = {}

        self.initial_renderer()

    def initial_renderer(self):
        self.create_widgets()
        self.update_ui()

    def create_widgets(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.pack(fill="both", expand=True)

        self.main_frame.columnconfigure(0, weight=3)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)

        # Left frame (cookie button and stats)
        self.left_frame = ttk.Frame(self.main_frame, padding=10)
        self.left_frame.grid(row=0, column=0, sticky=tk.NSEW)

        self.left_frame.columnconfigure(0, weight=1)
        self.left_frame.rowconfigure(0, weight=0)
        self.left_frame.rowconfigure(1, weight=0)
        self.left_frame.rowconfigure(2, weight=1)

        # Stats frame and widgets
        self.stats_frame = ttk.Frame(self.left_frame)
        self.stats_frame.grid(row=0, column=0, sticky=tk.N, pady=(10, 5))

        # Cookies label
        self.cookies_label = ttk.Label(
            self.stats_frame, text="0 cookies", font=("Segoe UI", 24)
        )
        self.cookies_label.grid(row=0, column=0)

        # Cookies per second label
        self.cps_label = ttk.Label(
            self.stats_frame, text="0 cookies per sec", font=("Segoe UI", 12)
        )
        self.cps_label.grid(row=1, column=0)

        # Cookie button (left frame)
        self.cookie_img = tk.PhotoImage(file="assets/cookie.png")
        self.cookie_button = ttk.Button(
            self.left_frame,
            image=self.cookie_img,
            padding=20,
            command=self.on_cookie_click,
        )
        self.cookie_button.grid(row=1, column=0, pady=(5, 10))

        # Right frame (upgrades)
        self.right_frame = ttk.Frame(self.main_frame, padding=25)
        self.right_frame.grid(row=0, column=1, sticky=tk.NSEW)

        self.right_frame.columnconfigure(0, weight=1)
        self.right_frame.rowconfigure(1, weight=1)

        # 'Upgrades' title
        ttk.Label(
            self.right_frame, text="Upgrades", font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        self.upgrades_container = ttk.Frame(self.right_frame)
        self.upgrades_container.grid(row=1, column=0, sticky=tk.NSEW)
        self.upgrades_container.columnconfigure(0, weight=1)

        for upgrade in self.upgrades:
            self.create_upgrade(
                upgrade.name,
                "0",
                upgrade.effect,
                upgrade.base_cost,
                upgrade.upgrade_type,
                upgrade.id,
            )

    def create_upgrade(
        self,
        name: str,
        current_prod: str,
        effect: str,
        cost: int,
        upgrade_type: str,
        row: int,
    ):
        # Main frame for each individual upgrade
        frame = ttk.Frame(self.upgrades_container, padding=10, relief="ridge")
        frame.grid(row=row, column=0, sticky=tk.EW, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)

        # Name
        name_label = ttk.Label(
            frame, text=f"{name} (x0)", font=("Segoe UI", 11, "bold")
        )
        name_label.grid(row=0, column=0, sticky=tk.W)

        name = name.lower()
        formatted_upgrade_type = (
            upgrade_type.upper() if upgrade_type == "cps" else upgrade_type
        )

        # Cost (on the right)
        cost_label = ttk.Label(frame, text=f"Cost: {cost}")
        cost_label.grid(row=0, column=1, sticky=tk.E, padx=(12, 0))

        # Current production
        production_label = ttk.Label(
            frame,
            text=f"Current: +{current_prod} {formatted_upgrade_type}",
            font=("Segoe UI", 10),
        )
        production_label.grid(row=1, column=0, sticky=tk.W, pady=(2, 0))

        # Effect each new one has
        effect_label = ttk.Label(
            frame,
            text=f"+{effect} {formatted_upgrade_type} per {name}",
            font=("Segoe UI", 10),
            foreground="gray",
        )
        effect_label.grid(row=2, column=0, sticky=tk.W, pady=(4, 0))

        # Buy button (on the right)
        buy_button = ttk.Button(
            frame, text="Buy", command=lambda: self.on_buy_click(name)
        )
        buy_button.grid(row=1, column=1, rowspan=2, sticky=tk.E, padx=(12, 0))

        # Save all widgets for easier manipulation later
        self.upgrade_widgets[name] = {
            "name_label": name_label,
            "cost_label": cost_label,
            "production_label": production_label,
            "effect_label": effect_label,
            "buy_button": buy_button,
        }

    def update_ui(self):
        self.update_cookie_count()
        self.update_cps()
        self.update_upgrades()

    def update_cookie_count(self):
        pass

    def update_cps(self):
        pass

    def update_upgrades(self):
        pass

    def update_button_states(self):
        pass

    def on_cookie_click(self):
        self.game_manager.click()

    def on_buy_click(self, upgrade: str):
        print(f"Upgrade bought: {upgrade}")
