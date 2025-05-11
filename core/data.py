# core/data.py
from pathlib import Path
import json

DATA_FILE = Path("todos.json")

def load_data():
    if not DATA_FILE.exists():
        return {"meta": {}, "todos": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_id(todos):
    used_ids = {item['id'] for item in todos}
    i = 1
    while i in used_ids:
        i += 1
    return i