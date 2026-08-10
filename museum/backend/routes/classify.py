import time

from fastapi import APIRouter, HTTPException

from backend.schemas import SubmitFactRequest, ClassificationResponse
from backend.services.classify_service import classify
from backend.services.facts_store import add_submitted

router = APIRouter()


@router.post("/classify", response_model=ClassificationResponse)
def classify_endpoint(req: SubmitFactRequest):
    start = time.perf_counter()
    try:
        result = classify(req.fact)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    latency_ms = (time.perf_counter() - start) * 1000
    exhibit_id = f"S{int(time.time()) % 100000:05d}"

    add_submitted({
        "id": exhibit_id,
        "fact": result.fact,
        "category": result.category,
        "weirdness": result.weirdness,
        "wtf": result.wtf,
        "tags": result.tags,
        "source": "visitor submission",
        "confidence": result.confidence,
    })

    return ClassificationResponse(
        fact=result.fact,
        category=result.category,
        category_emoji=result.category_emoji,
        weirdness=result.weirdness,
        wtf=result.wtf,
        confidence=result.confidence,
        tags=result.tags,
        explanation=result.explanation,
        model_notes=result.model_notes,
        latency_ms=round(latency_ms, 2),
        exhibit_id=exhibit_id,
        accepted=True,
    )