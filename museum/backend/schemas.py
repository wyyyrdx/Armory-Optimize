from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class SubmitFactRequest(BaseModel):
    fact: str = Field(..., min_length=10, max_length=500)

    @field_validator("fact")
    @classmethod
    def clean(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Fact cannot be empty")
        return v


class ClassificationResponse(BaseModel):
    fact: str
    category: str
    category_emoji: str
    weirdness: int
    wtf: int
    confidence: float
    tags: List[str]
    explanation: str
    model_notes: str
    latency_ms: float
    exhibit_id: Optional[str] = None
    accepted: bool = True