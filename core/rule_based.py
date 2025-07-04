
from core.data import fragrance_db

family_to_note = {
    "Fruity": "top",
    "Citrus": "top",
    "Floral": "middle",
    "Spicy": "middle",
    "Gourmand": "base",
    "Woody": "base",
    "Musk": "base",
    "Mix": None
}

def get_heuristic_notes(chemicals: dict) -> dict:
    notes = {"top": [], "middle": [], "base": [], "unknown": []}
    for name, pct in chemicals.items():
        chem = fragrance_db.get(name)
        if chem:
            note = chem["note"] or family_to_note.get(chem["family"], None)
            if note:
                notes[note].append(name)
            else:
                notes["unknown"].append(name)
        else:
            notes["unknown"].append(name)
    return notes
