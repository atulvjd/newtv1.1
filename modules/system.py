import os
import subprocess
import ctypes
import datetime
import platform
import pyautogui
import win32gui
import win32con
import win32clipboard
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, ISimpleAudioVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from core.speech import speak


# ===================== AUDIO CONTROLS =====================

def set_master_volume(level):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        scalar = float(level) / 100.0
        volume.SetMasterVolumeLevelScalar(scalar, None)
        print(f"🔊 Master volume set to {level}%")
    except Exception as e:
        print(f"❌ Error setting master volume: {e}")
        speak("Failed to adjust master volume.")

def get_master_volume():
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        scalar = volume.GetMasterVolumeLevelScalar()
        return int(scalar * 100)
    except Exception as e:
        print(f"❌ Error getting volume: {e}")
        return -1

def mute_system(mute=True):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMute(int(mute), None)
        speak("System muted." if mute else "System unmuted.")
    except Exception as e:
        print(f"❌ Error muting system: {e}")

def set_app_volume(app_name, level):
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and app_name.lower() in session.Process.name().lower():
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                volume.SetMasterVolume(level / 100.0, None)
                speak(f"{app_name} volume set to {level}%.")
                return
        speak(f"No running app named {app_name} found.")
    except Exception as e:
        print(f"❌ Error setting volume for {app_name}: {e}")

def mute_app(app_name, mute=True):
    try:
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and app_name.lower() in session.Process.name().lower():
                volume = session._ctl.QueryInterface(ISimpleAudioVolume)
                volume.SetMute(int(mute), None)
                speak(f"{app_name} muted." if mute else f"{app_name} unmuted.")
                return
        speak(f"App {app_name} not found.")
    except Exception as e:
        print(f"❌ Error muting {app_name}: {e}")


# ===================== POWER ACTIONS =====================

def shutdown_system():
    speak("Shutting down now.")
    os.system("shutdown /s /t 0")

def restart_system():
    speak("Restarting the system.")
    os.system("shutdown /r /t 0")

def lock_system():
    speak("Locking your PC.")
    ctypes.windll.user32.LockWorkStation()

def cancel_shutdown():
    os.system("shutdown /a")
    speak("Scheduled shutdown canceled.")

def hibernate_system():
    speak("Hibernating your PC.")
    os.system("shutdown /h")

def sleep_system():
    speak("Putting your system to sleep.")
    os.system("rundll32.exe powrprof.dll,SetSuspendState Sleep")


# ===================== SCREEN & UI =====================

def take_screenshot():
    try:
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        path = f"screenshots/screenshot_{timestamp}.png"
        pyautogui.screenshot(path)
        speak("Screenshot captured.")
        print(f"📸 Saved at: {path}")
    except Exception as e:
        speak("Failed to capture screenshot.")
        print(f"❌ Screenshot error: {e}")

def minimize_all_windows():
    hwnd = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hwnd, win32con.SW_FORCEMINIMIZE)
    speak("Minimized all windows.")

def open_task_manager():
    subprocess.Popen("taskmgr")
    speak("Opening Task Manager.")

def open_control_panel():
    subprocess.Popen("control")
    speak("Opening Control Panel.")

def open_settings():
    subprocess.Popen("start ms-settings:", shell=True)
    speak("Opening Settings.")

def show_system_info():
    subprocess.Popen("msinfo32")
    speak("Opening system information.")

def open_registry_editor():
    subprocess.Popen("regedit")
    speak("Opening Registry Editor.")

def open_file_explorer():
    subprocess.Popen("explorer")
    speak("Opening File Explorer.")


# ===================== SYSTEM TOOLS =====================

def adjust_brightness(level: int):
    try:
        # Requires: `MonitorBright.exe` or WMI module
        os.system(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})")
        speak(f"Brightness set to {level} percent.")
    except Exception as e:
        speak("I couldn't adjust brightness.")
        print(f"❌ Brightness error: {e}")

def empty_recycle_bin():
    try:
        os.system("powershell Clear-RecycleBin -Force")
        speak("Recycle bin emptied.")
    except Exception as e:
        speak("Failed to empty recycle bin.")
        print(f"❌ Recycle Bin Error: {e}")

def clean_temp_files():
    try:
        temp = os.environ.get("TEMP", "C:\\Windows\\Temp")
        os.system(f'del /q /s "{temp}\\*"')
        speak("Temporary files cleaned.")
    except Exception as e:
        speak("Error cleaning temporary files.")
        print(f"❌ Temp cleanup error: {e}")

def copy_to_clipboard(text):
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()
        speak("Copied to clipboard.")
    except Exception as e:
        speak("Failed to copy to clipboard.")
        print(f"❌ Clipboard error: {e}")

def show_ip_address():
    os.system("ipconfig")
    speak("Here’s your IP configuration.")

def get_os_info():
    info = f"{platform.system()} {platform.release()}, version {platform.version()}"
    speak(f"You're running {info}")
    return info

