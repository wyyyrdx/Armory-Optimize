import random
from typing import Optional

from fastapi import APIRouter, HTTPException

from backend.services.facts_store import all_exhibits, get_by_id
from ml.categories import CATEGORIES, EMOJI

router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok", "exhibits": len(all_exhibits())}


@router.get("/categories")
def categories():
    return {
        "categories": [
            {"name": c, "emoji": EMOJI.get(c, "🎲")} for c in CATEGORIES
        ]
    }


@router.get("/exhibits")
def list_exhibits(
    category: Optional[str] = None,
    sort: str = "weirdness",
    limit: int = 100,
):
    items = all_exhibits()

    if category and category != "All":
        items = [e for e in items if e.get("category") == category]

    if sort == "weirdness":
        items = sorted(items, key=lambda x: x.get("weirdness", 0), reverse=True)
    elif sort == "wtf":
        items = sorted(items, key=lambda x: x.get("wtf", 0), reverse=True)
    elif sort == "id":
        items = sorted(items, key=lambda x: str(x.get("id", "")))

    return {"count": len(items), "exhibits": items[:limit]}


@router.get("/exhibits/{exhibit_id}")
def one_exhibit(exhibit_id: str):
    item = get_by_id(exhibit_id)
    if not item:
        raise HTTPException(status_code=404, detail="Exhibit not found")
    return item


@router.get("/random")
def random_exhibit():
    items = all_exhibits()
    if not items:
        raise HTTPException(status_code=404, detail="No exhibits")
    return random.choice(items)