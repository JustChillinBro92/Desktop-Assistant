import subprocess
import shutil

from core.steam_resolver import scan_installed_games, find_game


# -----------------------------
# Desktop app aliases
# -----------------------------
APP_ALIASES = {
    "chrome": ["chrome", "browser", "google chrome"],
    "vscode": ["vscode", "vs code", "code"],
    "spotify": ["spotify", "music"],
    "notepad": ["notepad"],
    "explorer": ["file explorer", "files"],
    "discord": ["discord"],
    "steam": ["steam"]
}

ALIAS_TO_APP = {}
for app, aliases in APP_ALIASES.items():
    for a in aliases:
        ALIAS_TO_APP[a] = app


# -----------------------------
# Open desktop app
# -----------------------------
def open_app(app: str):
    path = shutil.which(app)

    if path:
        subprocess.Popen(path)
    else:
        subprocess.Popen(f"start {app}", shell=True)


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
# MAIN ROUTER (context preserved)
# -----------------------------
def open_something(command: dict):
    cmd_type = command.get("type")
    target = command.get("app") or command.get("game") or ""

    target = target.lower().strip()

    print(f"[ROUTER] type={cmd_type}, target={target}")

    # -------------------------
    # OPEN APP
    # -------------------------
    if cmd_type == "open_app":
        # verify app exists via alias system
        for alias, app in ALIAS_TO_APP.items():
            if alias in target:
                open_app(app)
                return

        # fallback attempt
        open_app(target)
        return

    # -------------------------
    # OPEN GAME
    # -------------------------
    elif cmd_type == "open_game":
        open_game(target)
        return

    # -------------------------
    # UNKNOWN SAFETY
    # -------------------------
    else: 
        print("[BLOCKED] Unknown or unsupported command")