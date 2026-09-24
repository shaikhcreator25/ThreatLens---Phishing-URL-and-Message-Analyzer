"""
PhishGuard AI — Message Analyzer

Deterministic, rule-based NLP analysis of suspicious messages.
Detects phishing indicators using keyword/pattern matching and
returns an explainable risk score with reasons.

Structured so an LLM (Gemini / OpenAI) can be added later without
changing the return contract.
"""

import re
from typing import Any, Dict, List, Tuple


# ---------------------------------------------------------------------------
# Pattern definitions
# Each entry: (compiled regex, score contribution, human-readable reason)
# ---------------------------------------------------------------------------

_PATTERNS: List[Tuple[re.Pattern, int, str]] = [
    # Urgency
    (
        re.compile(
            r"\b(urgent|immediately|right\s+now|act\s+now|hurry|asap|"
            r"within\s+\d+\s*(hours?|minutes?|days?)|time\s+is\s+running\s+out|"
            r"don'?t\s+delay|expires?\s+(today|soon|now)|last\s+chance|"
            r"final\s+(warning|notice|reminder))\b",
            re.IGNORECASE,
        ),
        15,
        "Urgency language detected in message",
    ),
    # Account suspension / threats
    (
        re.compile(
            r"\b(suspend(ed)?|deactivat(ed|e|ion)|terminat(ed|e|ion)|"
            r"lock(ed)?(\s+out)?|restrict(ed)?|disabled?|compromised|"
            r"unauthori[sz]ed\s+(access|activity|transaction)|breach(ed)?)\b",
            re.IGNORECASE,
        ),
        20,
        "Account suspension or security threat language detected",
    ),
    # Credential requests
    (
        re.compile(
            r"\b(enter\s+your\s+(password|credentials|login)|"
            r"(provide|confirm|verify|update|validate)\s+(your\s+)?(password|credentials|login|username)|"
            r"sign[\s-]?in\s+(details|information|credentials))\b",
            re.IGNORECASE,
        ),
        25,
        "Request for login credentials detected",
    ),
    # OTP / password / PIN requests
    (
        re.compile(
            r"\b(otp|one[\s-]?time\s+(password|code|pin)|"
            r"verification\s+code|security\s+code|"
            r"(enter|provide|share|send)\s+(your\s+)?(pin|otp|password|passcode)|"
            r"two[\s-]?factor|2fa|mfa)\b",
            re.IGNORECASE,
        ),
        30,
        "Request for OTP, PIN, or password detected",
    ),
    # Click / verify requests
    (
        re.compile(
            r"\b(click\s+(here|below|the\s+link|this\s+link)|"
            r"verify\s+(your\s+)?(account|identity|email|information)|"
            r"(account|identity|email)\s+verification|"
            r"requires?\s+verification|"
            r"review\s+(your\s+)?(account|information|details)|"
            r"confirm\s+(your\s+)?(account|identity|email|information)|"
            r"update\s+(your\s+)?(account|profile|information|details)|"
            r"log\s*in\s+(to\s+)?(verify|confirm|secure))\b",
            re.IGNORECASE,
        ),
        15,
        "Request to click a link or verify account information",
    ),
    # Financial requests
    (
        re.compile(
            r"\b(bank\s+(account|details|information)|"
            r"(credit|debit)\s+card|card\s+number|cvv|"
            r"(wire|bank)\s+transfer|payment\s+(details|information)|"
            r"billing\s+(address|information|details)|"
            r"(send|transfer|pay)\s+\$?\d+|"
            r"social\s+security|ssn|routing\s+number)\b",
            re.IGNORECASE,
        ),
        20,
        "Request for financial or banking information detected",
    ),
    # Prize / reward scams
    (
        re.compile(
            r"\b(congratulations|you('ve|\s+have)\s+won|"
            r"(claim|collect)\s+(your\s+)?(prize|reward|gift|bonus|winnings)|"
            r"lucky\s+(winner|draw|customer)|"
            r"free\s+(gift|iphone|ipad|macbook|laptop|money|cash)|"
            r"lottery|sweepstakes|giveaway)\b",
            re.IGNORECASE,
        ),
        15,
        "Fake prize or reward language detected",
    ),
    # Impersonation indicators
    (
        re.compile(
            r"\b(dear\s+(customer|user|member|account\s+holder|valued\s+customer)|"
            r"(this\s+is|from)\s+(the\s+)?(security|support|admin|IT)\s+(team|department|desk)|"
            r"official\s+(notice|communication|notification)|"
            r"on\s+behalf\s+of\s+(your\s+)?(bank|company|organization)|"
            r"(apple|google|microsoft|amazon|paypal|netflix|facebook|instagram|"
            r"whatsapp|telegram)\s+(support|security|team|service))\b",
            re.IGNORECASE,
        ),
        15,
        "Possible impersonation of a trusted entity",
    ),
    # Fear / pressure
    (
        re.compile(
            r"\b(legal\s+action|law\s+enforcement|police|arrest(ed)?|"
            r"prosecut(ed|ion)|court\s+order|warrant|"
            r"failure\s+to\s+(comply|respond|verify)|"
            r"permanent(ly)?\s+(lock|delet|clos|suspend)|"
            r"lose\s+access|"
            r"(will|shall)\s+be\s+(closed|deleted|suspended|terminated|locked))\b",
            re.IGNORECASE,
        ),
        10,
        "Fear or pressure tactics detected",
    ),
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def analyze_message(message: Any) -> Dict[str, Any]:
    """Analyze a message for phishing indicators.

    Args:
        message: The suspicious message text to analyze.

    Returns:
        dict with keys:
            score  (int 0-100): risk score
            reasons (list[str]): human-readable explanations
    """
    # --- Edge cases ---
    if message is None:
        return {"score": 0, "reasons": []}

    if not isinstance(message, str):
        message = str(message)

    text = message.strip()
    if not text:
        return {"score": 0, "reasons": []}

    # Truncate extremely long messages to prevent regex DoS
    text = text[:10_000]

    # --- Run pattern checks ---
    score = 0
    reasons: List[str] = []

    for pattern, weight, reason in _PATTERNS:
        if pattern.search(text):
            score += weight
            if reason not in reasons:
                reasons.append(reason)

    # Cap score at 100
    score = min(score, 100)

    return {"score": score, "reasons": reasons}
