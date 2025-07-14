import os
import json
from core.speech import speak

MEMORY_FILE = "data/memory.json"

# Ensure memory file exists
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump([], f)

def _load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Memory Load Error] {e}")
        return []

def _save_memory(memory_list):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory_list, f, indent=2)
    except Exception as e:
        print(f"[Memory Save Error] {e}")

def add_to_memory(info: str):
    info = info.strip()
    if not info:
        speak("You didn’t say what to remember.")
        return
    memory_list = _load_memory()
    memory_list.append(info)
    _save_memory(memory_list)
    speak(f"I’ve remembered that: {info}")

def list_memory():
    memory_list = _load_memory()
    if not memory_list:
        speak("I don’t remember anything yet.")
        return
    speak("Here’s what I remember:")
    for i, item in enumerate(memory_list, start=1):
        speak(f"{i}. {item}")

def clear_memory():
    _save_memory([])
    speak("I’ve cleared all remembered items.")
