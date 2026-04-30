import subprocess
import json


def get_uwp_apps():
    """
    Fetch all installed UWP apps from Windows
    """
    try:
        output = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "Get-StartApps | ConvertTo-Json"
            ],
            text=True
        )

        data = json.loads(output)

        # PowerShell returns dict if only 1 app, list otherwise
        if isinstance(data, dict):
            data = [data]

        apps = {}

        for app in data:
            name = app.get("Name", "").lower().strip()
            app_id = app.get("AppID", "")

            if name and app_id:
                apps[name] = app_id

        return apps

    except Exception as e:
        print("[UWP SCAN ERROR]", e)
        return {}
    
UWP_CACHE = get_uwp_apps()
# print(UWP_CACHE)