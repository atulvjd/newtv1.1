import json
import os
from core.speech import speak

COMMAND_FILE = os.path.join("data", "custom_commands.json")

# Ensure the data folder and command file exist
os.makedirs(os.path.dirname(COMMAND_FILE), exist_ok=True)
if not os.path.exists(COMMAND_FILE):
    with open(COMMAND_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

def load_custom_commands():
    """Load all stored custom commands."""
    try:
        with open(COMMAND_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        speak("I found a corrupted custom command file. Resetting it.")
        with open(COMMAND_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    except Exception as e:
        print(f"[❌ load_custom_commands error] {e}")
        return {}

def save_custom_commands(data):
    """Save custom commands to file."""
    try:
        with open(COMMAND_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[❌ save_custom_commands error] {e}")

def teach_new_command(trigger_phrase, command_sequence):
    """
    Teach a new custom command.
    :param trigger_phrase: the phrase that will trigger this action.
    :param command_sequence: a list of commands to execute.
    """
    trigger_phrase = trigger_phrase.lower().strip()
    if not trigger_phrase or not command_sequence:
        speak("The command or its action was empty. Please try again.")
        return

    if not isinstance(command_sequence, list):
        speak("The command sequence must be a list of commands.")
        return

    data = load_custom_commands()
    data[trigger_phrase] = command_sequence
    save_custom_commands(data)
    speak(f"Got it. When you say '{trigger_phrase}', I'll run {len(command_sequence)} step{'s' if len(command_sequence) > 1 else ''}.")

def execute_custom_command(command):
    """
    Execute a previously taught custom command.
    Returns True if a custom command was found and executed.
    """
    # Import handle_command locally here to avoid circular import
    from core.task_router import handle_command

    command = command.lower().strip()
    data = load_custom_commands()

    if command in data:
        steps = data[command]
        if not isinstance(steps, list):
            speak("This command seems broken. I'll skip it for now.")
            return False
        speak(f"Running your custom routine for '{command}'.")
        for step in steps:
            try:
                handle_command(step)
            except Exception as e:
                print(f"[⚠️ Command execution error]: {step} | Error: {e}")
        return True
    return False
