import json
import os

COMMAND_FILE = os.path.join("data", "custom_commands.json")

# === File Utilities ===

def ensure_command_file():
    """Ensure the custom command file exists and is properly initialized."""
    os.makedirs(os.path.dirname(COMMAND_FILE), exist_ok=True)
    if not os.path.exists(COMMAND_FILE):
        with open(COMMAND_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

def load_custom_commands():
    """Load all custom commands from JSON file."""
    ensure_command_file()
    try:
        with open(COMMAND_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        return {}

def save_custom_commands(data):
    """Save updated custom commands to file."""
    with open(COMMAND_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# === Core Functions ===

def add_custom_command(trigger_phrase: str, action_list: list[str]):
    """Teach a new command trigger with a list of actions."""
    trigger = trigger_phrase.strip().lower()
    data = load_custom_commands()
    data[trigger] = [a.strip() for a in action_list]
    save_custom_commands(data)

def check_and_expand_custom_command(command: str) -> list[str] | None:
    """
    Check if a command is a learned custom trigger.
    Returns: list of actions if match found, else None.
    """
    command = command.strip().lower()
    data = load_custom_commands()
    return data.get(command, None)
