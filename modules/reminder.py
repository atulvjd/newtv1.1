# modules/reminder.py

import os
import json
import time
import threading
import datetime
from core.speech import speak

try:
    from win10toast import ToastNotifier
    notifier = ToastNotifier()
    TOAST_AVAILABLE = True
except ImportError:
    TOAST_AVAILABLE = False
    notifier = None

REMINDER_FILE = "data/reminders.json"

def load_reminders():
    if not os.path.exists(REMINDER_FILE):
        return []
    try:
        with open(REMINDER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Error loading reminders] {e}")
        return []

def save_reminders(reminders):
    os.makedirs(os.path.dirname(REMINDER_FILE), exist_ok=True)
    with open(REMINDER_FILE, "w", encoding="utf-8") as f:
        json.dump(reminders, f, indent=2)

def add_reminder(task, time_str):
    reminders = load_reminders()
    
    # Prevent duplicate reminders
    for r in reminders:
        if r["task"].strip().lower() == task.strip().lower() and r["time"] == time_str:
            speak("This reminder already exists.")
            return

    reminders.append({"task": task.strip(), "time": time_str})
    save_reminders(reminders)
    speak(f"Reminder set for {task} at {time_str}")

def get_due_reminders():
    now = datetime.datetime.now()
    due = []
    for r in load_reminders():
        try:
            rt = datetime.datetime.strptime(r["time"], "%Y-%m-%d %H:%M")
            if rt <= now:
                due.append(r)
        except Exception as e:
            print(f"[Reminder time parse error] {e}")
    return due

def remove_reminder(reminder):
    reminders = load_reminders()
    new_list = [r for r in reminders if not (r["task"] == reminder["task"] and r["time"] == reminder["time"])]
    save_reminders(new_list)

def reminder_checker():
    while True:
        try:
            due_list = get_due_reminders()
            for reminder in due_list:
                task = reminder["task"]
                speak(f"⏰ Reminder: {task}")
                if TOAST_AVAILABLE:
                    notifier.show_toast("Newt Reminder", task, duration=10, threaded=True)
                remove_reminder(reminder)
        except Exception as e:
            print(f"[Reminder Thread Error] {e}")
        time.sleep(60)  # Check every 60 seconds

def start_reminder_loop():
    try:
        t = threading.Thread(target=reminder_checker, daemon=True)
        t.start()
        print("🔔 Reminder loop started.")
    except Exception as e:
        print(f"[Reminder Loop Error] {e}")
        speak("Reminder loop couldn't start.")

def list_reminders():
    reminders = load_reminders()
    if not reminders:
        speak("You have no reminders.")
        return

    upcoming = []
    now = datetime.datetime.now()

    for r in reminders:
        try:
            r_time = datetime.datetime.strptime(r["time"], "%Y-%m-%d %H:%M")
            if r_time >= now:
                upcoming.append((r_time, r["task"]))
        except:
            continue

    if not upcoming:
        speak("You have no upcoming reminders.")
    else:
        speak(f"You have {len(upcoming)} upcoming reminder{'s' if len(upcoming) > 1 else ''}:")
        for r_time, task in sorted(upcoming):
            date_str = r_time.strftime("%I:%M %p on %B %d")
            speak(f"{task} at {date_str}")
