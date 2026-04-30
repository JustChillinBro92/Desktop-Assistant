import os
import re

STEAM_APPS_FOLDER = r"C:\Program Files (x86)\Steam\steamapps"


# -----------------------------
# 1. Parse appmanifest file
# -----------------------------
def parse_manifest(file_path):
    app_id = None
    name = None

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

            # Extract appid
            app_id_match = re.search(r'"appid"\s+"(\d+)"', content)
            if app_id_match:
                app_id = app_id_match.group(1)

            # Extract game name
            name_match = re.search(r'"name"\s+"(.+?)"', content)
            if name_match:
                name = name_match.group(1).lower()

    except:
        pass

    return name, app_id


# -----------------------------
# 2. Scan installed Steam games
# -----------------------------
def scan_installed_games():
    games = {}

    if not os.path.exists(STEAM_APPS_FOLDER):
        print("[ERROR] Steam folder not found")
        return games

    for file in os.listdir(STEAM_APPS_FOLDER):
        if file.startswith("appmanifest") and file.endswith(".acf"):
            name, app_id = parse_manifest(
                os.path.join(STEAM_APPS_FOLDER, file)
            )

            if name and app_id:
                games[name] = app_id

    return games


# -----------------------------
# 3. Match user input to game
# -----------------------------
def find_game(user_input, games_dict):
    user_input = user_input.lower()

    best_match = None
    best_id = None

    for name, app_id in games_dict.items():
        # simple substring match (can upgrade later to fuzzy matching)
        if user_input in name or name in user_input:
            return app_id

        # keep fallback candidate
        if any(word in name for word in user_input.split()):
            best_match = name
            best_id = app_id

    return best_id