"""
DAXDA.IA — FastAPI Application Entry Point
Nicole Protocol / 886-Ops Architecture
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI(
    title="DAXDA.IA — Nicole Protocol",
    description=(
        "DAXDA.IA 886-Ops Mode: a 16-layer recursive governance runtime in which each layer "
        "executes 55 atomic audit tiles, followed by 6 final system authority operations. "
        "Its purpose is not merely to produce an answer, but to produce a traceable, "
        "stress-tested, evidence-aware, contradiction-scanned, recursively governable answer "
        "with explicit authority boundaries."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
