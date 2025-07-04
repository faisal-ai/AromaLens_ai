import json
import os

def load_presets(file_path: str = "..data/presets.json") -> dict:
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as f:
        return json.load(f)
