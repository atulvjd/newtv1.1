from core.speech import speak
from core.memory import Memory
from core.nlp_parser import preprocess
from memory.context_memory import add_to_memory, list_memory, clear_memory
from modules.reminder import add_reminder, list_reminders
from modules.timer import start_timer, cancel_timer
from modules.file_manager import create_folder, delete_file, search_files, open_folder
from modules.custom_commands import teach_new_command, execute_custom_command
from modules import open_apps, browser_automation, spotify_control, system

import datetime
import os
import subprocess
import pyautogui
import psutil
from dateutil import parser as date_parser
import re

memory = Memory()

def handle_command(command: str):
    command = preprocess(command.lower().strip())
    if not command:
        speak("Please say a command.")
        return

    # === APP LAUNCH ===
    if command.startswith(("open", "start", "launch")):
        for prefix in ["open", "start", "launch"]:
            if command.startswith(prefix):
                app_name = command[len(prefix):].strip()
                if app_name:
                    try:
                        open_apps.launch_app(app_name)
                        speak(f"Opening {app_name}.")
                    except Exception as e:
                        print(f"[App Launch Error] {e}")
                        speak(f"Failed to open {app_name}.")
                else:
                    speak("Please specify the app name.")
                return

    # === CUSTOM COMMANDS ===
    if command.startswith("next time i say"):
        try:
            parts = command[len("next time i say"):].strip()
            if "do" in parts:
                trigger, actions = parts.split("do", 1)
                trigger = trigger.strip().strip("'\"")
                actions_list = [a.strip() for a in actions.split(" and ")]
                teach_new_command(trigger, actions_list)
                speak(f"Got it. When you say '{trigger}', I will do {', '.join(actions_list)}.")
            else:
                speak("Please tell me what to do after the trigger.")
        except Exception as e:
            print(f"[Teach Error] {e}")
            speak("I couldn’t understand that. Try again.")
        return

    if execute_custom_command(command):
        return

    # === MEMORY ===
    if command.startswith("remember that"):
        info = command[len("remember that"):].strip()
        if info:
            add_to_memory(info)
            speak("Okay, I've remembered that.")
        else:
            speak("What would you like me to remember?")
        return

    if "clear memory" in command or "delete memory" in command:
        clear_memory()
        speak("Memory cleared.")
        return

    if "what do you remember" in command or "what's in memory" in command or "show memory" in command:
        list_memory()
        return

    # === REMINDERS ===
    if "remind me" in command:
        handle_reminder_command(command)
        return

    if "what are my reminders" in command or "list reminders" in command or "upcoming reminders" in command:
        list_reminders()
        return

    # === TIMER ===
    if "start timer" in command or "start countdown" in command:
        match = re.search(r"\b(\d+)\s*(minute|minutes)?", command)
        minutes = int(match.group(1)) if match else 1
        start_timer(minutes)
        speak(f"Timer started for {minutes} minute{'s' if minutes != 1 else ''}.")
        return

    if "cancel timer" in command or "stop timer" in command:
        cancel_timer()
        speak("Timer cancelled.")
        return

    # === BATTERY / TIME / DATE ===
    if "battery" in command:
        battery = psutil.sensors_battery()
        if battery:
            plugged = "plugged in" if battery.power_plugged else "not plugged in"
            speak(f"Battery is at {battery.percent} percent and is {plugged}.")
        else:
            speak("Couldn't get battery info.")
        return

    if "time" in command:
        now = datetime.datetime.now()
        speak(f"The current time is {now.strftime('%I:%M %p')}.")
        return

    if "date" in command:
        today = datetime.datetime.now()
        speak(f"Today's date is {today.strftime('%B %d, %Y')}.")
        return

    # === SCREENSHOT ===
    if "take screenshot" in command or "capture screen" in command:
        try:
            os.makedirs("screenshots", exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"screenshots/screenshot_{timestamp}.png"
            pyautogui.screenshot(path)
            speak(f"Screenshot saved as {path}.")
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
            speak("Failed to take screenshot.")
        return

    # === SYSTEM ACTIONS ===
    if any(k in command for k in ["shutdown", "restart", "lock", "sleep", "hibernate", "cancel shutdown"]):
        try:
            system.handle_system_command(command)
            speak("System command executed.")
        except Exception as e:
            print(f"[System Command Error] {e}")
            speak("Failed to execute system command.")
        return

    # === VOLUME CONTROLS ===
    if "set volume to" in command:
        try:
            level_str = command.split("set volume to")[-1].replace("%", "").strip()
            level = int(level_str)
            system.set_master_volume(level)
            speak(f"Volume set to {level} percent.")
        except Exception:
            speak("Please say a valid volume level.")
        return

    if "mute system" in command:
        system.mute_system(True)
        speak("System muted.")
        return

    if "unmute system" in command:
        system.mute_system(False)
        speak("System unmuted.")
        return

    for app in ["spotify", "brave"]:
        if f"set {app} volume to" in command:
            try:
                level_str = command.split(f"set {app} volume to")[-1].replace("%", "").strip()
                level = int(level_str)
                system.set_app_volume(app, level)
                speak(f"{app.capitalize()} volume set to {level} percent.")
            except Exception:
                speak("Please say a valid volume level.")
            return

        if f"mute {app}" in command:
            system.mute_app(app, True)
            speak(f"{app.capitalize()} muted.")
            return

        if f"unmute {app}" in command:
            system.mute_app(app, False)
            speak(f"{app.capitalize()} unmuted.")
            return

    # === FILE MANAGEMENT ===
    if "create folder" in command:
        parts = command.split("create folder")[-1].strip()
        if " in " in parts:
            folder, location = parts.split(" in ", 1)
            create_folder(folder.strip(), location.strip())
            speak(f"Created folder {folder.strip()} in {location.strip()}.")
        else:
            create_folder(parts.strip())
            speak(f"Created folder {parts.strip()}.")
        return

    if "delete" in command:
        parts = command.split("delete")[-1].strip()
        if " from " in parts:
            filename, location = parts.split(" from ", 1)
            delete_file(filename.strip(), location.strip())
            speak(f"Deleted {filename.strip()} from {location.strip()}.")
        else:
            delete_file(parts.strip())
            speak(f"Deleted {parts.strip()}.")
        return

    if "search" in command and "file" in command:
        parts = command.split("search for")[-1].strip()
        if " in " in parts:
            ext, location = parts.split(" in ", 1)
            search_files(ext.strip(), location.strip())
            speak(f"Searching for {ext.strip()} files in {location.strip()}.")
        else:
            search_files(parts.strip())
            speak(f"Searching for {parts.strip()} files.")
        return

    if "open folder" in command:
        folder = command.split("open folder")[-1].strip()
        open_folder(folder)
        speak(f"Opened folder {folder}.")
        return

    # === KNOWN FILE LOCATIONS ===
    file_paths = {
        "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
        "documents": os.path.join(os.path.expanduser("~"), "Documents"),
        "desktop": os.path.join(os.path.expanduser("~"), "Desktop")
    }
    for key, path in file_paths.items():
        if f"open {key}" in command:
            try:
                os.startfile(path)
                speak(f"Opened {key}.")
            except Exception as e:
                print(f"[Open Folder Error] {e}")
                speak(f"Failed to open {key}.")
            return

    # === SYSTEM TOOLS ===
    tools = {
        "control panel": "control",
        "task manager": "taskmgr",
        "terminal": "cmd",
        "powershell": "powershell",
        "system info": "msinfo32",
        "registry editor": "regedit",
        "calculator": "calc",
        "notepad": "notepad",
        "paint": "mspaint",
        "snipping tool": "snippingtool",
        "file explorer": "explorer",
        "settings": ["start", "ms-settings:"]
    }
    for key, cmd in tools.items():
        if f"open {key}" in command:
            try:
                subprocess.Popen(cmd)
                speak(f"Opened {key}.")
            except Exception as e:
                print(f"[Open Tool Error] {e}")
                speak(f"Failed to open {key}.")
            return

    # === SPOTIFY CONTROLS ===
    if "pause spotify" in command:
        spotify_control.pause()
        speak("Spotify paused.")
        return

    if "play spotify" in command:
        spotify_control.play()
        speak("Spotify playing.")
        return

    if "next song" in command:
        spotify_control.next_track()
        speak("Playing next song.")
        return

    if "previous song" in command:
        spotify_control.previous_track()
        speak("Playing previous song.")
        return

    if "play song" in command:
        song = command.replace("play song", "").strip()
        if song:
            spotify_control.play_song(song)
            speak(f"Playing song {song}.")
        else:
            speak("What song do you want me to play?")
        return

    # === BROWSER AUTOMATION ===
    if "search" in command:
        browser_automation.handle_search_command(command)
        return

    if "youtube" in command and "play" in command:
        browser_automation.play_youtube_video(command)
        return

    if "open" in command and ".com" in command:
        browser_automation.open_custom_website(command)
        return

    # === FALLBACK ===
    speak("Sorry, I didn’t understand that command.")


def handle_reminder_command(command):
    try:
        if "remind me to" in command:
            parts = command.split("remind me to")[1].strip()
            if " at " in parts:
                task, time_str = parts.rsplit(" at ", 1)
            elif " tomorrow " in parts:
                task, time_str = parts.split(" tomorrow ", 1)
                time_str = "tomorrow " + time_str
            else:
                speak("Please include a time for the reminder.")
                return

            reminder_time = date_parser.parse(time_str, fuzzy=True)
            formatted = reminder_time.strftime("%Y-%m-%d %H:%M")
            add_reminder(task.strip(), formatted)
            speak(f"Reminder set for {task.strip()} at {reminder_time.strftime('%I:%M %p on %B %d')}.")
        else:
            speak("I didn't catch the reminder task.")
    except Exception as e:
        print(f"[Reminder Error] {e}")
        speak("There was an issue setting your reminder.")
