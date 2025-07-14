from flask import Flask, render_template, request, redirect
import json
import os
from datetime import datetime

app = Flask(__name__)
MEMORY_FILE = "../data/memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try:
                data = json.load(f)
                return data if isinstance(data, list) else []
            except json.JSONDecodeError:
                return []
    return []

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text")
        if text:
            memory = load_memory()
            memory.append({
                "text": text.strip(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            save_memory(memory)
        return redirect("/")

    memory = load_memory()
    return render_template("index.html", memory=memory)

@app.route("/delete/<int:index>")
def delete(index):
    memory = load_memory()
    if 0 <= index < len(memory):
        memory.pop(index)
        save_memory(memory)
    return redirect("/")

@app.route("/clear")
def clear():
    save_memory([])
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
