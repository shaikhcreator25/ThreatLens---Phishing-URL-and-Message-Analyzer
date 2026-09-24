"""Tests for the FastAPI /analyze and /health endpoints."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthEndpoint:
    def test_health(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"


class TestAnalyzeEndpoint:
    def test_phishing_message_and_url(self):
        response = client.post(
            "/analyze",
            json={
                "message": "URGENT! Your bank account will be suspended. Verify immediately!",
                "url": "http://192.168.1.50/login/verify-account",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] in ("SAFE", "SUSPICIOUS", "PHISHING")
        assert 0 <= data["risk_score"] <= 100
        assert 0 <= data["message_score"] <= 100
        assert 0 <= data["url_score"] <= 100
        assert isinstance(data["reasons"], list)

    def test_message_only(self):
        response = client.post(
            "/analyze",
            json={"message": "Your account has been compromised. Enter your password now."},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["url_score"] == 0
        assert data["message_score"] > 0

    def test_url_only(self):
        response = client.post(
            "/analyze",
            json={"url": "http://192.168.1.50/login"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message_score"] == 0
        assert data["url_score"] > 0

    def test_missing_both(self):
        response = client.post("/analyze", json={})
        assert response.status_code == 422

    def test_empty_strings(self):
        response = client.post("/analyze", json={"message": "", "url": ""})
        assert response.status_code == 422

    def test_safe_message(self):
        response = client.post(
            "/analyze",
            json={"message": "Hey, are we still meeting at 5 PM today?"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["classification"] == "SAFE"

    def test_response_has_all_fields(self):
        response = client.post(
            "/analyze",
            json={"message": "Test message", "url": "https://example.com"},
        )
        assert response.status_code == 200
        data = response.json()
        for field in ("classification", "risk_score", "message_score", "url_score", "reasons"):
            assert field in data

    def test_reasons_are_limited(self):
        response = client.post(
            "/analyze",
            json={
                "message": (
                    "URGENT! Your account has been suspended. Enter your password "
                    "and OTP immediately. Click here to verify your bank account. "
                    "Congratulations! This is Apple Security Team. Legal action!"
                ),
                "url": "http://192.168.1.1:9999@evil.com/login/verify/account",
            },
        )
        data = response.json()
        assert len(data["reasons"]) <= 7
