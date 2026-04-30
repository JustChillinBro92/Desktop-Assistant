import subprocess
 
from core.uwp_scanner import UWP_CACHE
from core.app_scanner import APP_CACHE, find_best_match
from core.steam_resolver import scan_installed_games, find_game



# -----------------------------
# OPEN PATH
# -----------------------------
def open_path(app_name, app_info):
    path = app_info["path"]
    source = app_info["source"]

    app_name = app_name.lower().strip()

    # UWP handling
    if source == "uwp":
        query = app_name.replace(" ", "")

        for name, app_id in UWP_CACHE.items():
            normalized_name = name.lower().replace(" ", "")

            if query in normalized_name:
                print(f"[UWP] Launching → {name}\n")
                subprocess.Popen(f'explorer.exe shell:AppsFolder\\{app_id}', shell=True)
                return

        print("[UWP] No match found", "\n")
        return
    
    # normal apps
    print(f"[APP] Launching → {app_name}\n")
    subprocess.Popen(f'start "" "{path}"', shell=True)



# -----------------------------
# Open desktop app
# -----------------------------
def open_app(app_name: str):
    app_name = app_name.lower().strip()
    print(f"[APP RESOLVER] Searching for: {app_name}")

    gui_apps = {
        k: v for k, v in APP_CACHE.items() 
        if v["source"] in ["start_menu", "desktop", "uwp"]
    }
    path_apps = {
        k: v for k, v in APP_CACHE.items() 
        if v["source"] == "path"
    }

    # 1. exact GUI match
    if app_name in gui_apps:
        print(f"[APP FOUND] Exact GUI match → {app_name}")
        open_path(app_name, gui_apps[app_name])
        return True
    
    # 2. UWP DIRECT LOOKUP
    query = app_name.replace(" ", "")

    for name, app_id in UWP_CACHE.items():
        normalized = name.lower().replace(" ", "")

        if query in normalized:
            print(f"[UWP] Launching → {name}\n")
            subprocess.Popen(
                f'explorer.exe shell:AppsFolder\\{app_id}',
                shell=True
            )
            return True

    # 3 fuzzy GUI match
    match = find_best_match(app_name, gui_apps)
    if match:
        print(f"[APP] Fuzzy GUI match → {match}")
        open_path(match, gui_apps[match])
        return True

    # 4. exact PATH match
    if app_name in path_apps:
        print(f"[APP FOUND] Exact PATH match → {app_name}")
        open_path(app_name, path_apps[app_name])
        return True

    # 5. final system fallback
    try:
        print("[APP FALLBACK] Trying system fallback...\n")
        subprocess.Popen(f"start {app_name}", shell=True)
        return True
    except Exception as e:
        print("[FALLBACK ERROR]", e, "\n")

    # 6. app not found
    print("[BLOCKED] App not found\n")
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