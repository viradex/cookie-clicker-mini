CPS_MULTIPLIER = 1.15

UI_UPDATE_FREQUENCY = 50
TITLE_UPDATE_FREQUENCY = 50
SAVE_FREQUENCY = 10000

FRENZY_DELAY_MIN = 15000
FRENZY_DELAY_MAX = 30000

FRENZY_DURATION_MIN = 5000
FRENZY_DURATION_MAX = 12000

POSSIBLE_FRENZY_MULTIPLIERS = (3, 5, 7, 10)
FRENZY_MISS_DELAY = 13000

MAKE_SAVE_FILE_READONLY = True

UPGRADES_DEFAULT_DATA = {
    0: {
        "name": "Cursor",
        "base_cost": 10,
        "effect": 1,
        "upgrade_type": "click",
    },
    1: {
        "id": 1,
        "name": "Worker",
        "base_cost": 50,
        "effect": 5,
        "upgrade_type": "cps",
    },
    2: {
        "id": 2,
        "name": "Farm",
        "base_cost": 200,
        "effect": 25,
        "upgrade_type": "cps",
    },
    3: {
        "id": 3,
        "name": "Factory",
        "base_cost": 500,
        "effect": 125,
        "upgrade_type": "cps",
    },
}
