import os
import json
from datetime import datetime
from core.speech import speak

MEMORY_JSON = "data/memory.json"
MEMORY_JSONL = "data/memory.jsonl"

class Memory:
    def __init__(self):
        os.makedirs("data", exist_ok=True)
        self._init_file(MEMORY_JSON, default=[])
        self._init_file(MEMORY_JSONL)

    def _init_file(self, path, default=None):
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                if default is not None:
                    json.dump(default, f, indent=2)
                else:
                    pass  # JSONL doesn't need initial content

    def _load_memory_json(self):
        try:
            with open(MEMORY_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Memory Load Error] {e}")
            return []

    def _save_memory_json(self, data):
        try:
            with open(MEMORY_JSON, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[Memory Save Error] {e}")

    def _append_jsonl(self, text):
        try:
            with open(MEMORY_JSONL, "a", encoding="utf-8") as f:
                record = {
                    "input": text.strip(),
                    "timestamp": datetime.now().isoformat()
                }
                f.write(json.dumps(record) + "\n")
        except Exception as e:
            print(f"[JSONL Save Error] {e}")

    def remember(self, text: str):
        text = text.strip()
        if not text:
            speak("You didn’t say what to remember.")
            return

        memory_list = self._load_memory_json()
        memory_list.append({
            "text": text,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        self._save_memory_json(memory_list)
        self._append_jsonl(text)
        speak("Got it. I’ve remembered that.")

    def list_memory(self):
        memory_list = self._load_memory_json()
        if not memory_list:
            speak("I don’t remember anything yet.")
            return
        speak(f"I have {len(memory_list)} things in memory.")
        for entry in memory_list:
            timestamp = entry.get("timestamp", "unknown time")
            speak(f"{entry['text']} — added on {timestamp}")

    def clear_memory(self):
        self._save_memory_json([])
        speak("All memories have been cleared.")
