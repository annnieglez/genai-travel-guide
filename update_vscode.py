import os
import json
import platform

def update_vscode_settings():
    # Determine the platform and set the appropriate path for VS Code settings.json
    if platform.system() == "Windows":
        vscode_settings_path = os.path.expandvars(r"%APPDATA%\Code\User\settings.json")
    else:
        vscode_settings_path = os.path.expanduser("~/.config/Code/User/settings.json")
    
    try:
        # Load existing settings or create a new dictionary
        if os.path.exists(vscode_settings_path):
            with open(vscode_settings_path, "r") as f:
                settings = json.load(f)
        else:
            settings = {}

        # Update the python.analysis.extraPaths setting
        extra_paths = settings.get("python.analysis.extraPaths", [])
        project_path = os.path.abspath(os.path.dirname(__file__))

        if project_path not in extra_paths:
            extra_paths.append(project_path)
            
        settings["python.analysis.extraPaths"] = extra_paths


        # Add or update additional settings
        settings["python.languageServer"] = "Pylance"
        settings["python.analysis.autoSearchPaths"] = True
        settings["python.analysis.useLibraryCodeForTypes"] = True

        # Write the updated settings back to the file
        with open(vscode_settings_path, "w") as f:
            json.dump(settings, f, indent=4)
        print("VS Code settings.json updated successfully.")
    except Exception as e:
        print(f"Failed to update VS Code settings.json: {e}")

if __name__ == "__main__":
    update_vscode_settings()
