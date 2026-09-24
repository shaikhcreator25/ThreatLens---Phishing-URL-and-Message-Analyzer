"""
PhishGuard AI — Risk Engine

Combines the scores from the message analyzer and URL analyzer into a
single risk assessment with a classification, overall score, and
deduplicated, prioritized list of reasons.
"""

from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Classification thresholds (prototype heuristics, not validated)
# ---------------------------------------------------------------------------

_THRESHOLD_SAFE = 34
_THRESHOLD_SUSPICIOUS = 69
# Anything above _THRESHOLD_SUSPICIOUS → PHISHING

_MESSAGE_WEIGHT = 0.45
_URL_WEIGHT = 0.55
_MAX_REASONS = 7


def _classify(score: int) -> str:
    """Map a 0–100 score to a classification label."""
    if score <= _THRESHOLD_SAFE:
        return "SAFE"
    if score <= _THRESHOLD_SUSPICIOUS:
        return "SUSPICIOUS"
    return "PHISHING"


def calculate_risk(
    message_result: Optional[Dict[str, Any]] = None,
    url_result: Optional[Dict[str, Any]] = None,
    threat_intel_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Combine analyzer results into a final risk assessment.

    Args:
        message_result: Output of ``analyze_message()``, or ``None``.
        url_result:     Output of ``analyze_url()``, or ``None``.
        threat_intel_result: Output of ``check_url_reputation()``, or ``None``.

    Returns:
        dict matching the ``AnalyzeResponse`` schema:
            classification (str), risk_score (int),
            message_score (int), url_score (int), reasons (list[str])
    """
    message_score: int = (message_result or {}).get("score", 0)
    url_score: int = (url_result or {}).get("score", 0)

    message_reasons: List[str] = (message_result or {}).get("reasons", [])
    url_reasons: List[str] = (url_result or {}).get("reasons", [])

    if threat_intel_result and threat_intel_result.get("known_malicious"):
        url_score = 100
        url_reasons.insert(0, f"Threat Intel: {threat_intel_result.get('reason')}")

    # --- Compute final score ---
    has_message = message_result is not None and message_score > 0 or (message_result is not None and len(message_reasons) > 0)
    has_url = url_result is not None and url_score > 0 or (url_result is not None and len(url_reasons) > 0)

    if has_message and has_url:
        weighted = message_score * _MESSAGE_WEIGHT + url_score * _URL_WEIGHT
        # Ensure one high-risk component isn't diluted by a low-risk one
        component_floor = max(message_score, url_score) * 0.7
        final_score = max(weighted, component_floor)
    elif has_message:
        final_score = float(message_score)
    elif has_url:
        final_score = float(url_score)
    else:
        final_score = 0.0

    final_score = max(0, min(100, round(final_score)))

    # --- Merge & deduplicate reasons ---
    seen: set = set()
    combined_reasons: List[str] = []
    for reason in message_reasons + url_reasons:
        if reason not in seen:
            seen.add(reason)
            combined_reasons.append(reason)

    # Limit to the most relevant reasons
    combined_reasons = combined_reasons[:_MAX_REASONS]

    return {
        "classification": _classify(final_score),
        "risk_score": final_score,
        "message_score": message_score,
        "url_score": url_score,
        "reasons": combined_reasons,
    }
