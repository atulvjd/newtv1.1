# main.py (Offline version – LLM disabled)

from core.speech import speak
from core.voice_interface import listen_command
from core.task_router import handle_command
from modules.reminder import start_reminder_loop  # 🔔 Background reminder notifier

def main():
    # Start the reminder notification thread (non-blocking)
    start_reminder_loop()

    # Greet the user on startup
    speak("Hello! How can I assist you today?")

    try:
        while True:
            command = listen_command()
            if command:
                print(f"Command received: {command}")
                handle_command(command)
            else:
                # Optional: prompt if no command detected after a pause
                # speak("I didn't catch that. Please say your command again.")
                pass
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C exit
        speak("Goodbye! Have a great day.")
    except Exception as e:
        # Log and notify errors without crashing
        print(f"Error: {e}")
        speak("I encountered an error while processing your command. Please try again.")

if __name__ == "__main__":
    main()
