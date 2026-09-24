"""
PhishGuard AI — FastAPI Backend

Exposes the /analyze and /health endpoints.
All analysis is delegated to the independent analyzers and risk engine.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import AnalyzeRequest, AnalyzeResponse, HealthResponse
from analyzers.message_analyzer import analyze_message
from analyzers.url_analyzer import analyze_url
from analyzers.threat_intel import check_url_reputation
from risk_engine import calculate_risk


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="ThreatLens",
    description="AI-powered phishing detection with explainable risk analysis",
    version="1.0.0",
)

# CORS — allow the local Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Simple liveness probe."""
    return HealthResponse(status="ok")


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    """Analyze a suspicious message and/or URL for phishing indicators."""

    # Validation: at least one input required
    if request.message is None and request.url is None:
        raise HTTPException(
            status_code=422,
            detail="At least one of 'message' or 'url' must be provided.",
        )

    # Run analyzers
    message_result = None
    url_result = None

    if request.message is not None:
        message_result = analyze_message(request.message)

    threat_intel_result = None

    if request.url is not None:
        url_result = analyze_url(request.url)
        threat_intel_result = check_url_reputation(request.url)

    # Combine via risk engine
    result = calculate_risk(
        message_result=message_result,
        url_result=url_result,
        threat_intel_result=threat_intel_result,
    )

    return AnalyzeResponse(**result)
