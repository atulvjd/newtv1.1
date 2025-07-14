import time
import threading
from datetime import timedelta
from core.speech import speak

active_timer = None
timer_cancelled = threading.Event()

# ========== Helper Utilities ==========

def format_time(seconds):
    return str(timedelta(seconds=int(seconds)))

def parse_time(input_str):
    input_str = input_str.lower()
    mins, secs = 0, 0

    if "min" in input_str:
        try:
            mins = int(input_str.split("min")[0].strip())
        except:
            pass
    if "sec" in input_str:
        try:
            sec_part = input_str.split("sec")[0]
            if "min" in sec_part:
                secs = int(sec_part.split("min")[-1].strip())
            else:
                secs = int(sec_part.strip())
        except:
            pass

    total = mins * 60 + secs
    return total if total > 0 else 60  # Default 60s if parsing fails


# ========== Timer Logic ==========

def _run_countdown(seconds):
    timer_cancelled.clear()
    start_time = time.time()
    end_time = start_time + seconds

    try:
        while time.time() < end_time:
            if timer_cancelled.is_set():
                speak("Timer cancelled.")
                return
            time.sleep(1)
        speak("⏰ Time's up!")
    except Exception as e:
        speak("Timer failed to complete.")
        print(f"❌ Timer error: {e}")

def start_timer(duration="1 min"):
    global active_timer

    if active_timer and active_timer.is_alive():
        speak("A timer is already running.")
        return

    seconds = parse_time(duration)
    speak(f"Timer started for {format_time(seconds)}.")
    active_timer = threading.Thread(target=_run_countdown, args=(seconds,), daemon=True)
    active_timer.start()

def cancel_timer():
    global active_timer
    if active_timer and active_timer.is_alive():
        timer_cancelled.set()
        speak("Timer cancelled.")
        active_timer = None
    else:
        speak("There is no active timer running.")


# ========== Stopwatch Logic ==========

stopwatch_start = None
stopwatch_thread = None
stopwatch_running = threading.Event()

def _run_stopwatch():
    global stopwatch_start
    stopwatch_start = time.time()
    stopwatch_running.set()
    speak("Stopwatch started.")
    try:
        while stopwatch_running.is_set():
            time.sleep(1)
    except:
        speak("Stopwatch error.")

def start_stopwatch():
    global stopwatch_thread
    if stopwatch_running.is_set():
        speak("Stopwatch is already running.")
        return
    stopwatch_thread = threading.Thread(target=_run_stopwatch, daemon=True)
    stopwatch_thread.start()

def stop_stopwatch():
    if not stopwatch_running.is_set():
        speak("Stopwatch is not running.")
        return

    stopwatch_running.clear()
    elapsed = time.time() - stopwatch_start
    speak(f"⏱ Stopwatch stopped at {format_time(elapsed)}.")


# ========== Timer Voice Summary (for status check) ==========

def timer_status():
    if active_timer and active_timer.is_alive() and not timer_cancelled.is_set():
        speak("A timer is currently running.")
    elif stopwatch_running.is_set():
        elapsed = time.time() - stopwatch_start
        speak(f"Stopwatch running. Elapsed time: {format_time(elapsed)}.")
    else:
        speak("No active timers or stopwatch.")
