from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.services.facts_store import load_facts
from backend.routes import exhibits, classify, arm


def create_app() -> FastAPI:
    app = FastAPI(
        title="Museum of Useless Knowledge",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    load_facts()

    app.include_router(exhibits.router, prefix="/api")
    app.include_router(classify.router, prefix="/api")
    app.include_router(arm.router, prefix="/api")

    return app