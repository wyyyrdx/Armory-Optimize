import re
import hashlib
from dataclasses import dataclass, asdict

from ml.categories import CATEGORIES, EMOJI, KEYWORDS


@dataclass
class Result:
    fact: str
    category: str
    category_emoji: str
    weirdness: int
    wtf: int 
    confidence: float
    tags: list
    explanation: str
    model_notes: str = "Playful museum scores. Not a scientific instrument."

    def to_dict(self):
        return asdict(self)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _hash01(text: str, salt: str) -> float:
    """Stable number between 0 and 1 from text (same input => same output)."""
    h = hashlib.sha256((salt + text).encode()).hexdigest()
    return int(h[:8], 16) / 0xFFFFFFFF


def predict_category(text: str):
    text_n = _normalize(text)
    scores = {c: 0.0 for c in CATEGORIES}

    for cat, words in KEYWORDS.items():
        for w in words:
            if re.search(r"\b" + re.escape(w) + r"\b", text_n):
                scores[cat] += 2.0

    
    if any(w in text_n for w in ["heart", "brain", "poop", "breathe"]):
        scores["Animals"] += 1.5
    if any(w in text_n for w in ["planet", "moon", "orbit"]):
        scores["Space"] += 2.0

    best = max(scores, key=scores.get)
    max_score = scores[best]

    if max_score < 1:
        best = "Random / Other"
        confidence = 0.45 + 0.15 * _hash01(text_n, "cat")
    else:
        total = sum(scores.values()) or 1.0
        confidence = min(0.97, 0.55 + (max_score / total) * 0.4)

    tags = []
    for cat, words in KEYWORDS.items():
        if cat == best:
            continue
        if any(re.search(r"\b" + re.escape(w) + r"\b", text_n) for w in words):
            tags.append(cat.lower())

    return best, round(confidence, 3), tags[:4]


def score_weirdness(text: str) -> int:
    text_n = _normalize(text)
    score = 62.0

    length = len(text)
    if 40 <= length <= 120:
        score += 10
    elif length > 120:
        score += 5
    else:
        score += 3

    markers = ["but", "actually", "longer than", "more than", "before", "never", "only"]
    score += min(20, sum(5 for m in markers if m in text_n))

    if re.search(r"\d", text):
        score += 7

    if any(w in text_n for w in ["poop", "butt", "hearts", "brains", "breathe", "immortal"]):
        score += 14

    score += (_hash01(text_n, "weird") - 0.5) * 8
    return int(max(45, min(99, round(score))))


def score_freak(text: str, weirdness: int) -> int:
    text_n = _normalize(text)
    base = weirdness * 0.92

    visceral = ["poop", "butt", "blood", "heart", "brain", "breathe", "immortal"]
    base += sum(5 for v in visceral if v in text_n)

    if any(w in text_n for w in ["three hearts", "cube-shaped", "breathe through"]):
        base += 10

    base += (_hash01(text_n, "freak") - 0.5) * 6
    return int(max(50, min(99, round(base))))


def classify_fact(fact: str) -> Result:
    fact = fact.strip()
    if not fact:
        raise ValueError("Empty fact")
    if len(fact) > 500:
        raise ValueError("Fact too long (max 500 characters)")

    category, confidence, tags = predict_category(fact)
    weirdness = score_weirdness(fact)
    freak = score_freak(fact, weirdness)

    explanation = (
        f"The curator placed this under {category}. "
        f"Weirdness {weirdness}/100 and Freak {freak}/100 are playful museum scores."
    )

    return Result(
        fact=fact,
        category=category,
        category_emoji=EMOJI.get(category, "🎲"),
        weirdness=weirdness,
        wtf=freak,
        confidence=confidence,
        tags=tags,
        explanation=explanation,
    )