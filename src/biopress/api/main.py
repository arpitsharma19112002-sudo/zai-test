"""FastAPI application for BioPress."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from biopress.api.routes import generate, validate, pdf

app = FastAPI(
    title="BioPress API",
    description="REST API for BioPress Designer - Educational content generation",
    version="0.1.0",
)

allowed_origins = os.getenv(
    "CORS_ORIGINS", 
    "http://localhost:3000,http://localhost:8000,http://localhost:8080"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(generate.router, prefix="/api/v1", tags=["generate"])
app.include_router(validate.router, prefix="/api/v1", tags=["validate"])
app.include_router(pdf.router, prefix="/api/v1", tags=["pdf"])


@app.get("/")
def health():
    return {"status": "ok", "service": "biopress"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "biopress"}

# NOTE: The custom /docs endpoint that was here has been removed.
# FastAPI's built-in Swagger UI at /docs now works correctly.