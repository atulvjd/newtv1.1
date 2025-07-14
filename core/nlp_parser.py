import os
import json

NLP_RULES_FILE = "data/nlp_rules.json"

# Load rules
def load_nlp_rules():
    if not os.path.exists(NLP_RULES_FILE):
        return {
            "junk_phrases": [],
            "synonyms": {},
            "command_aliases": {},
            "start_patterns": {},
            "fallback_prefix": ""
        }
    with open(NLP_RULES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

rules = load_nlp_rules()

def preprocess(command: str) -> str:
    command = command.lower().strip()

    # 1. Remove junk phrases
    for junk in rules["junk_phrases"]:
        if junk in command:
            command = command.replace(junk, "").strip()

    # 2. Replace synonyms (e.g., "run" → "open")
    for word, replacement in rules["synonyms"].items():
        if word in command:
            command = command.replace(word, replacement)

    # 3. Expand aliases (e.g., "focus mode" → "open notepad and turn off wi-fi")
    if command in rules["command_aliases"]:
        return rules["command_aliases"][command]

    # 4. Normalize patterns (e.g., "search for", "look up")
    for pattern, replacement in rules["start_patterns"].items():
        if command.startswith(pattern):
            command = command.replace(pattern, replacement, 1).strip()

    # 5. Add fallback prefix (if defined)
    if rules.get("fallback_prefix") and not command.startswith(rules["fallback_prefix"]):
        command = rules["fallback_prefix"] + command

    return command
