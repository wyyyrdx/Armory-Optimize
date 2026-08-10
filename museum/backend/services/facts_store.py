import json
from typing import List, Optional

from backend.config import DATA_FILE

_FACTS: List[dict] = []
_SUBMITTED: List[dict] = []


def load_facts() -> None:
    global _FACTS
    _FACTS = []
    if not DATA_FILE.exists():
        print(f"WARNING: data file not found: {DATA_FILE}")
        return
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                _FACTS.append(json.loads(line))
    print(f"Loaded {len(_FACTS)} facts")


def all_exhibits() -> List[dict]:
    return _FACTS + _SUBMITTED


def get_by_id(exhibit_id: str) -> Optional[dict]:
    for item in all_exhibits():
        if item.get("id") == exhibit_id:
            return item
    return None


def add_submitted(item: dict) -> None:
    _SUBMITTED.append(item)