import tkinter as tk
from tkinter import ttk

from logic.number import abbreviate_number
from logic.game_manager import GameManager
from models.upgrade import Upgrade


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

    def update_ui(self):
        self.update_cookie_count()
        self.update_cps()
        self.update_frenzy_click_label()

        self.update_upgrades()
        self.update_button_states()

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
            self.stats_frame,
            text="0 cookies per sec",
            font=("Segoe UI", 12),
            anchor="center",
            justify="center",
        )
        self.cps_label.grid(row=1, column=0)

        # Cookie button (left frame)
        self.cookie_img = tk.PhotoImage(file="assets/cookie.png")
        self.cookie_frenzy_img = tk.PhotoImage(file="assets/cookie_gold_lg.png")

        self.cookie_button = ttk.Button(
            self.left_frame,
            image=self.cookie_img,
            padding=20,
            command=self.on_cookie_click,
        )
        self.cookie_button.grid(row=1, column=0, pady=(5, 10))

        # Click frenzy label
        self.frenzy_click_label = ttk.Label(
            self.left_frame,
            text="",
            font=("Segoe UI", 12, "bold"),
            foreground="#B8860B",
            anchor="center",
            justify="center",
        )
        # self.frenzy_click_label.grid(row=2, column=0, sticky=tk.N, pady=(5, 0))

        # Right frame (upgrades)
        self.right_frame = ttk.Frame(self.main_frame, padding=25)
        self.right_frame.grid(row=0, column=1, sticky=tk.NSEW)

        self.right_frame.columnconfigure(0, weight=2)
        self.right_frame.columnconfigure(1, weight=1)
        self.right_frame.rowconfigure(1, weight=1)

        # 'Upgrades' title
        ttk.Label(
            self.right_frame, text="Upgrades", font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        # Frenzy button
        self.frenzy_img = tk.PhotoImage(file="assets/cookie_gold.png")
        self.frenzy_button = ttk.Button(
            self.right_frame,
            image=self.frenzy_img,
            padding=5,
            command=self.on_frenzy_click,
        )
        # This line must be commented out to prevent it from showing when the app first runs
        # self.frenzy_button.grid(row=0, column=1, sticky=tk.E)

        # All upgrades
        self.upgrades_container = ttk.Frame(self.right_frame)
        self.upgrades_container.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.upgrades_container.columnconfigure(0, weight=1)

        self.no_upgrades_label = ttk.Label(
            self.upgrades_container,
            text="No upgrades yet...\nKeep clicking to unlock some!",
            font=("Segoe UI", 11, "italic"),
            foreground="gray",
            anchor="center",
            justify="center",
        )
        self.no_upgrades_label.grid(row=0, column=0, pady=20)

    def create_upgrade(self, upgrade: Upgrade):
        # Main frame for each individual upgrade
        frame = ttk.Frame(self.upgrades_container, padding=10, relief="ridge")
        frame.grid(row=upgrade.id, column=0, sticky=tk.EW, pady=5)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=0)

        # Name
        name_label = ttk.Label(
            frame, text=f"{upgrade.name} (x0)", font=("Segoe UI", 11, "bold")
        )
        name_label.grid(row=0, column=0, sticky=tk.W)

        name = upgrade.name.lower()

        # Cost (on the right)
        cost_label = ttk.Label(frame, text=f"Cost: {upgrade.get_cost()}")
        cost_label.grid(row=0, column=1, sticky=tk.E, padx=(12, 0))

        # Current production
        production_label = ttk.Label(
            frame,
            text=f"Current: +0 {upgrade.format_upgrade_type()}",
            font=("Segoe UI", 10),
        )
        production_label.grid(row=1, column=0, sticky=tk.W, pady=(2, 0))

        # Effect each new one has
        effect_label = ttk.Label(
            frame,
            text=f"+{upgrade.effect} {upgrade.format_upgrade_type()} per {name}",
            font=("Segoe UI", 10),
            foreground="gray",
        )
        effect_label.grid(row=2, column=0, sticky=tk.W, pady=(4, 0))

        # Buy button (on the right)
        buy_button = ttk.Button(
            frame, text="Buy", command=lambda: self.on_buy_click(upgrade.id)
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

    def update_cookie_count(self):
        cookies = self.game_manager.cookies
        self.cookies_label.config(text=f"{abbreviate_number(cookies)} cookies")

    def update_cps(self):
        cps = self.game_manager.get_total_cps()

        if self.game_manager.frenzy_active and self.game_manager.frenzy_type == "cps":
            self.cps_label.config(
                text=f"Frenzy (x{self.game_manager.frenzy_multiplier})!\n{abbreviate_number(cps)} cookies per sec",
                font=("Segoe UI", 12, "bold"),
                foreground="#B8860B",
            )
        else:
            self.cps_label.config(
                text=f"{abbreviate_number(cps)} cookies per sec",
                font=("Segoe UI", 12),
                foreground="black",
            )

    def update_frenzy_click_label(self):
        click = self.game_manager.get_click_power()

        if self.game_manager.frenzy_active and self.game_manager.frenzy_type == "click":
            self.frenzy_click_label.config(
                text=f"Frenzy (x{self.game_manager.frenzy_multiplier})!\n{abbreviate_number(click)} cookies per click"
            )
            self.frenzy_click_label.grid(row=2, column=0, sticky=tk.N, pady=(5, 0))
        else:
            self.frenzy_click_label.grid_forget()

    def update_upgrades(self):
        any_visible = False

        for upgrade in self.upgrades:
            if not upgrade.discovered:
                continue

            any_visible = True
            name = upgrade.name.lower()

            if name not in self.upgrade_widgets:
                self.create_upgrade(upgrade)

            widgets = self.upgrade_widgets[name]

            widgets["name_label"].config(text=f"{upgrade.name} (x{upgrade.amount})")

            widgets["cost_label"].config(
                text=f"Cost: {abbreviate_number(upgrade.get_cost())}"
            )

            if upgrade.upgrade_type == "click":
                value = upgrade.total_effect() + 1
            else:
                value = upgrade.total_effect()

            widgets["production_label"].config(
                text=f"Current: +{abbreviate_number(value)} {upgrade.format_upgrade_type()}"
            )

        if any_visible:
            self.no_upgrades_label.grid_forget()
        else:
            self.no_upgrades_label.grid(row=0, column=0, pady=20)

    def update_button_states(self):
        for upgrade in self.upgrades:
            if not upgrade.discovered:
                continue

            widgets = self.upgrade_widgets[upgrade.name.lower()]
            button = widgets["buy_button"]

            if self.game_manager.cookies >= upgrade.get_cost():
                button.config(state="normal")
            else:
                button.config(state="disabled")

    def show_frenzy_button(self):
        self.frenzy_button.grid(row=0, column=1, sticky=tk.E)

    def hide_frenzy_button(self):
        self.frenzy_button.grid_forget()

    def change_cookie_img(self, gold=False):
        if gold:
            self.cookie_button.config(image=self.cookie_frenzy_img)
        else:
            self.cookie_button.config(image=self.cookie_img)

    def on_cookie_click(self):
        self.game_manager.click()
        self.update_ui()

    def on_frenzy_click(self):
        self.frenzy_button.grid_forget()
        self.game_manager.start_frenzy()

        self.change_cookie_img(gold=True)
        self.root.on_frenzy_clicked()

    def on_buy_click(self, upgrade_id: int):
        success = self.game_manager.buy_upgrade(upgrade_id)
        if success:
            self.update_ui()
        else:
            print(f"Failed to buy upgrade '{upgrade_id}'")
