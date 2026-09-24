"""
PhishGuard AI — Pydantic Models

Defines the API request and response schemas used by the FastAPI backend.
These models serve as the integration contract between frontend and backend.
"""

from typing import List, Optional
from pydantic import BaseModel, field_validator


class AnalyzeRequest(BaseModel):
    """Request body for POST /analyze.

    At least one of `message` or `url` must be provided.
    """

    message: Optional[str] = None
    url: Optional[str] = None

    @field_validator("message", "url", mode="before")
    @classmethod
    def empty_string_to_none(cls, v):
        """Treat empty / whitespace-only strings as None."""
        if isinstance(v, str) and v.strip() == "":
            return None
        return v


class AnalyzeResponse(BaseModel):
    """Response body for POST /analyze."""

    classification: str  # "SAFE" | "SUSPICIOUS" | "PHISHING"
    risk_score: int  # 0–100
    message_score: int  # 0–100
    url_score: int  # 0–100
    reasons: List[str]


class HealthResponse(BaseModel):
    """Response body for GET /health."""

    status: str
