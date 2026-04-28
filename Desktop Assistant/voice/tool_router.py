from core.app_resolver import open_something

def run_tool(tool_name: str, args: dict):
    if tool_name == "open_app":
        app = args.get("app")

        open_something({
            "type": "open_app",
            "app": app
        })

        return {
            "status": "ok",
            "message": f"Opened app: {app}"
        }
    
    if tool_name == "open_game":
        game = args.get("game")

        open_something({
            "type": "open_game",
            "game": game
        })

        return {
            "status": "ok",
            "message": f"Opened app: {game}"
        }
    
    return {
        "status": "error",
        "message": f"Unknown Tool: {tool_name}"        
    }