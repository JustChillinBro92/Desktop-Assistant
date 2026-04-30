import os
from difflib import get_close_matches

# -----------------------------
# PATHS
# -----------------------------

START_MENU_PATHS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
]

DESKTOP_PATHS = [
    os.path.expandvars(r"%USERPROFILE%\Desktop"),
    r"C:\Users\Public\Desktop"
]



# -----------------------------
# START MENU SCAN
# -----------------------------
def scan_start_menu():
    apps = {}

    for base in START_MENU_PATHS:
        if not os.path.exists(base):
            continue

        for root, _, files in os.walk(base):
            for file in files:
                if file.endswith(".lnk"):
                    name = file.replace(".lnk", "").lower()
                    apps[name] = {
                        "path": os.path.join(root, file),
                        "source": "start_menu"
                    }

    return apps


# -----------------------------
# DESKTOP SCAN
# -----------------------------
def scan_desktop():
    apps = {}

    for base in DESKTOP_PATHS:
        if not os.path.exists(base):
            continue

        for file in os.listdir(base):
            if file.endswith(".lnk"):
                name = file.replace(".lnk", "").lower()
                apps[name] = {
                    "path": os.path.join(base, file),
                    "source": "desktop"
                }

    return apps

# -----------------------------
# PATH EXECUTABLES
# -----------------------------
def scan_path_apps():
    apps = {}

    for path in os.environ.get("PATH", "").split(os.pathsep):
        if not os.path.exists(path):
            continue

        try:
            for file in os.listdir(path):
                if file.endswith(".exe"):
                    name = file.replace(".exe", "").lower()
                    full_path = os.path.join(path, file)

                    if "WindowsApps" in full_path:
                        source = "uwp"  # treat as GUI
                    else:
                        source = "path"

                    apps[name] = {
                        "path": full_path,
                        "source": source
                    }
        except:
            continue

    return apps


# -----------------------------
# COMBINED SCAN
# -----------------------------
def scan_all_apps():
    apps = {}

    apps.update(scan_start_menu())
    apps.update(scan_desktop())
    apps.update(scan_path_apps())

    return apps

# -----------------------------
# FUZZY MATCH
# -----------------------------

def find_best_match(query, app_dict):
    names = list(app_dict.keys())
    matches = get_close_matches(query, names, n=1, cutoff=0.5)

    return matches[0] if matches else None

# cache for performance
APP_CACHE = scan_all_apps()
# print(APP_CACHE)
