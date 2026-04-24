import os
from difflib import get_close_matches

START_MENU_PATHS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
]


def scan_start_menu():
    apps = {}

    for base in START_MENU_PATHS:
        if not os.path.exists(base):
            continue

        for root, _, files in os.walk(base):
            for file in files:
                if file.endswith(".lnk"):
                    name = file.replace(".lnk", "").lower()
                    path = os.path.join(root, file)
                    apps[name] = path

    return apps


def find_best_match(query, app_dict):
    names = list(app_dict.keys())
    matches = get_close_matches(query, names, n=1, cutoff=0.5)

    return matches[0] if matches else None


# 🔥 OPTIONAL: cache for performance
APP_CACHE = scan_start_menu()