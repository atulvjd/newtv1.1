# modules/file_manager.py

import os
import shutil
import datetime
from core.speech import speak

# Predefined user directory mappings
USER_DIRS = {
    "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
    "documents": os.path.join(os.path.expanduser("~"), "Documents"),
    "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
    "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
    "music": os.path.join(os.path.expanduser("~"), "Music"),
    "videos": os.path.join(os.path.expanduser("~"), "Videos")
}

def get_base_path(location):
    """Return a user-friendly path based on location keyword."""
    return USER_DIRS.get(location.lower(), os.path.expanduser("~"))

def get_full_path(name, location="desktop"):
    base = get_base_path(location)
    return os.path.join(base, name)

# ========== CORE FILE OPERATIONS ==========

def create_folder(name, location="desktop"):
    path = get_full_path(name, location)
    try:
        os.makedirs(path, exist_ok=True)
        speak(f"Folder {name} created in {location}")
    except Exception as e:
        speak("I couldn't create the folder.")
        print(f"[❌ Create Folder Error] {e}")

def delete_file(name, location="desktop"):
    path = get_full_path(name, location)
    try:
        if os.path.isfile(path):
            os.remove(path)
            speak(f"File {name} deleted from {location}")
        elif os.path.isdir(path):
            shutil.rmtree(path)
            speak(f"Folder {name} deleted from {location}")
        else:
            speak("File or folder not found.")
    except Exception as e:
        speak("Error while deleting the file or folder.")
        print(f"[❌ Delete Error] {e}")

def rename_item(old_name, new_name, location="desktop"):
    old_path = get_full_path(old_name, location)
    new_path = get_full_path(new_name, location)
    try:
        os.rename(old_path, new_path)
        speak(f"Renamed {old_name} to {new_name}")
    except Exception as e:
        speak("I couldn't rename the item.")
        print(f"[❌ Rename Error] {e}")

def copy_item(name, destination_location="desktop", source_location="desktop"):
    source_path = get_full_path(name, source_location)
    dest_base = get_base_path(destination_location)
    dest_path = os.path.join(dest_base, name)
    try:
        if os.path.isfile(source_path):
            shutil.copy2(source_path, dest_path)
        elif os.path.isdir(source_path):
            shutil.copytree(source_path, dest_path)
        else:
            speak("File or folder not found.")
            return
        speak(f"{name} copied from {source_location} to {destination_location}")
    except Exception as e:
        speak("I couldn't copy the item.")
        print(f"[❌ Copy Error] {e}")

# ========== SEARCH & ACCESS ==========

def search_files(extension="", location="desktop"):
    base = get_base_path(location)
    results = []
    for root, _, files in os.walk(base):
        for file in files:
            if extension.lower() in file.lower():
                results.append(os.path.join(root, file))
    if results:
        speak(f"Found {len(results)} file{'s' if len(results) > 1 else ''} with {extension}")
        for r in results[:3]:  # only speak top 3
            speak(r)
    else:
        speak(f"No files with {extension} found in {location}.")

def open_folder(name, location="desktop"):
    path = get_full_path(name, location)
    if os.path.exists(path):
        try:
            os.startfile(path)
            speak(f"Opening folder {name}")
        except Exception as e:
            speak("Something went wrong while opening the folder.")
            print(f"[❌ Open Folder Error] {e}")
    else:
        speak("Folder not found.")

# ========== UTILITIES ==========

def list_directory(location="desktop"):
    base = get_base_path(location)
    try:
        items = os.listdir(base)
        if not items:
            speak(f"The {location} folder is empty.")
            return
        speak(f"There are {len(items)} items in {location}. Listing top five:")
        for item in items[:5]:
            speak(item)
    except Exception as e:
        speak(f"I couldn't list the contents of {location}.")
        print(f"[❌ List Directory Error] {e}")

def create_daily_log(log_name="log", location="documents"):
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    full_name = f"{log_name}_{now}.txt"
    path = get_full_path(full_name, location)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{now} - New log created.\n")
        speak(f"Daily log {full_name} created in {location}")
    except Exception as e:
        speak("Couldn't create the daily log.")
        print(f"[❌ Log Error] {e}")
