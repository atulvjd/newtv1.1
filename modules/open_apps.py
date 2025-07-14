# modules/open_apps.py

import os
import subprocess
import json
import platform
import shutil
from core.speech import speak

APP_PATHS_FILE = "data/app_paths.json"

def load_app_paths():
    """Load stored app paths."""
    if os.path.exists(APP_PATHS_FILE):
        try:
            with open(APP_PATHS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_app_paths(paths):
    """Save app paths."""
    os.makedirs(os.path.dirname(APP_PATHS_FILE), exist_ok=True)
    with open(APP_PATHS_FILE, 'w', encoding='utf-8') as f:
        json.dump(paths, f, indent=4)

def remember_app_path(app_name, path):
    """Store a new app path."""
    app_name = app_name.lower().strip()
    paths = load_app_paths()
    paths[app_name] = path
    save_app_paths(paths)
    speak(f"Got it. I’ve saved the path for {app_name}.")

def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

def try_direct_launch(app_name):
    """Try to launch using system path (fallback)."""
    try:
        if platform.system() == "Windows":
            subprocess.Popen(app_name, shell=True)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", app_name])
        else:  # Linux
            subprocess.Popen([app_name])
        print(f"🔄 Launched {app_name} via system launcher.")
        speak(f"Launching {app_name}")
        return True
    except Exception as e:
        print(f"❌ Direct launch failed: {e}")
        return False

def find_similar_app(app_name):
    """Try to match app name partially from saved paths."""
    paths = load_app_paths()
    for key in paths:
        if app_name.lower() in key:
            return paths[key]
    return None

def launch_app(app_name):
    """Main app launcher with fallbacks and memory."""
    app_name = app_name.lower().strip()
    paths = load_app_paths()

    # === 1. Exact match in saved paths
    if app_name in paths:
        path = paths[app_name]
        if os.path.exists(path):
            try:
                subprocess.Popen(path)
                print(f"🚀 Launching {app_name} from saved path.")
                speak(f"Launching {app_name}")
                return
            except Exception as e:
                speak(f"Failed to launch {app_name}. Trying system fallback.")
                print(f"[❌ Error] {e}")
        else:
            speak(f"The saved path for {app_name} seems broken. Trying fallback.")

    # === 2. Try a similar match from saved paths
    alt_path = find_similar_app(app_name)
    if alt_path and os.path.exists(alt_path):
        try:
            subprocess.Popen(alt_path)
            print(f"🚀 Launching {app_name} from similar match.")
            speak(f"Launching {app_name}")
            return
        except Exception as e:
            speak(f"Couldn't launch {app_name} from saved path.")
            print(f"[❌ Error] {e}")

    # === 3. Try direct launch via OS
    if try_direct_launch(app_name):
        return

    # === 4. Final fallback: suggest manual setup
    speak(f"I couldn't launch {app_name}. Please teach me its location.")
    print(f"⚠️ App '{app_name}' not found. Use remember_app_path() to teach me.")
