# utils.py
import json
from pathlib import Path

def load_word_replacements(path: str):
    """
    Load word/phrase replacements from a JSON file.
    Returns a dictionary: {misspelled_word: correct_word}
    """
    p = Path(path)
    if not p.exists():
        print(f"[WARNING] Word replacements file not found: {path}")
        return {}
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)

def apply_word_replacements(query: str, replacements: dict):
    """
    Apply word replacements to a query.
    Each token in the query is replaced if a mapping exists.
    Returns the processed query string.
    """
    tokens = query.split()
    replaced_tokens = [replacements.get(token.lower(), token) for token in tokens]
    return " ".join(replaced_tokens)