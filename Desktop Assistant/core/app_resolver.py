import subprocess
 
from core.app_scanner import APP_CACHE, find_best_match
from core.steam_resolver import scan_installed_games, find_game


# -----------------------------
# OPEN SHORTCUT
# -----------------------------
def open_shortcut(path):
    subprocess.Popen(path, shell=True)


# -----------------------------
# Open desktop app
# -----------------------------
def open_app(app_name: str):
    app_name = app_name.lower().strip()
    print(f"[APP RESOLVER] Searching for: {app_name}")

    apps = APP_CACHE

    # exact match
    if app_name in apps:
        print(f"[APP] Exact match → {app_name}")
        open_shortcut(apps[app_name])
        return True
    
    # fuzzy match
    match = find_best_match(app_name, apps)

    if match:
        print(f"[APP] Exact match → {match}")
        open_shortcut(apps[match])
        return True
    
    print("[BLOCKED] App not found")
    return False



# -----------------------------
# Open Steam game (ONLY if installed)
# -----------------------------
def open_game(game_name: str):
    games = scan_installed_games()
    app_id = find_game(game_name, games)

    if not app_id:
        print("[BLOCKED] Game not installed in Steam")
        return

    print(f"[STEAM] Launching game ID: {app_id}")
    subprocess.Popen(f"start steam://run/{app_id}", shell=True)


# -----------------------------
# MAIN ROUTER
# -----------------------------
def open_something(command: dict):
    cmd_type = command.get("type")
    target = command.get("app") or command.get("game") or ""

    target = target.lower().strip()

    print(f"[ROUTER] type={cmd_type}, target={target}")

    if cmd_type == "open_app":
        success = open_app(target)
        if not success:
            print("[FALLBACK] Could not find app")

    elif cmd_type == "open_game":
        open_game(target)

    else:
        print("[BLOCKED] Unknown or unsupported command")