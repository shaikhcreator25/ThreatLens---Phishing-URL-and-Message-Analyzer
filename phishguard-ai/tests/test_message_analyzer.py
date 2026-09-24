"""Tests for the message analyzer."""

import sys
import os

# Ensure the backend directory is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from analyzers.message_analyzer import analyze_message


class TestMessageAnalyzer:
    """Tests for analyze_message()."""

    def test_normal_message(self):
        result = analyze_message("Hey, are we still meeting at 5 PM today?")
        assert result["score"] < 40
        assert isinstance(result["reasons"], list)

    def test_urgent_phishing_message(self):
        result = analyze_message(
            "URGENT! Your bank account will be suspended today. "
            "Verify your account immediately using the link below."
        )
        assert result["score"] >= 40
        assert len(result["reasons"]) > 0

    def test_otp_request(self):
        result = analyze_message(
            "Enter your OTP to confirm the transaction on your account."
        )
        assert result["score"] >= 30
        assert any("OTP" in r or "PIN" in r or "password" in r for r in result["reasons"])

    def test_prize_scam(self):
        result = analyze_message(
            "Congratulations! You've won a free iPhone. "
            "Click here to claim your prize now!"
        )
        assert result["score"] >= 30
        assert any("prize" in r.lower() or "reward" in r.lower() for r in result["reasons"])

    def test_account_suspension_scam(self):
        result = analyze_message(
            "Your account has been suspended due to suspicious activity. "
            "Click the link below to restore access immediately."
        )
        assert result["score"] >= 40
        assert len(result["reasons"]) >= 2

    def test_empty_message(self):
        result = analyze_message("")
        assert result["score"] == 0
        assert result["reasons"] == []

    def test_none_message(self):
        result = analyze_message(None)
        assert result["score"] == 0
        assert result["reasons"] == []

    def test_whitespace_only(self):
        result = analyze_message("   \n\t  ")
        assert result["score"] == 0

    def test_score_capped_at_100(self):
        # A message with many phishing indicators
        result = analyze_message(
            "URGENT! Your account has been suspended. Enter your password "
            "and OTP immediately to verify your identity. Click here to "
            "confirm your bank account details. Congratulations, you've won "
            "a prize! This is from the Apple Security Team. Failure to "
            "comply will result in legal action."
        )
        assert result["score"] <= 100

    def test_mixed_case(self):
        result = analyze_message("VERIFY YOUR ACCOUNT IMMEDIATELY!")
        assert result["score"] > 0

    def test_no_duplicate_reasons(self):
        result = analyze_message(
            "Urgent! Act now! Hurry! Time is running out! ASAP!"
        )
        # All urgency words should collapse into one reason
        urgency_reasons = [r for r in result["reasons"] if "urgency" in r.lower()]
        assert len(urgency_reasons) <= 1

    def test_long_message(self):
        # Should handle without error
        long_message = "This is a normal message. " * 1000
        result = analyze_message(long_message)
        assert isinstance(result["score"], int)
