"""
PhishGuard AI — URL Analyzer

Deterministic, rule-based security feature analysis of suspicious URLs.
Inspects structural and lexical features to score phishing likelihood
and returns explainable reasons.

Uses only the Python standard library — no paid APIs required.
"""

import re
from typing import Any, Dict, List
from urllib.parse import urlparse, unquote


# ---------------------------------------------------------------------------
# Known URL shortener domains
# ---------------------------------------------------------------------------

_SHORTENERS = {
    "bit.ly", "tinyurl.com", "goo.gl", "t.co", "ow.ly", "is.gd",
    "buff.ly", "adf.ly", "bl.ink", "lnkd.in", "rb.gy", "cutt.ly",
    "shorturl.at", "tiny.cc", "x.co", "v.gd", "qr.ae",
}

# ---------------------------------------------------------------------------
# Suspicious keywords commonly found in phishing URLs
# ---------------------------------------------------------------------------

_SUSPICIOUS_KEYWORDS = [
    "login", "signin", "sign-in", "verify", "verification",
    "account", "secure", "security", "update", "confirm",
    "banking", "paypal", "wallet", "password", "credential",
    "authenticate", "suspend", "alert", "notification",
    "restore", "recover", "unlock", "validate",
]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def analyze_url(url: Any) -> Dict[str, Any]:
    """Analyze a URL for phishing indicators.

    Args:
        url: The suspicious URL string to analyze.

    Returns:
        dict with keys:
            score   (int 0-100): risk score
            reasons (list[str]): human-readable explanations
    """
    # --- Edge cases ---
    if url is None:
        return {"score": 0, "reasons": []}

    if not isinstance(url, str):
        url = str(url)

    url = url.strip()
    if not url:
        return {"score": 0, "reasons": []}

    # Truncate very long raw input to prevent abuse
    url = url[:2048]

    score = 0
    reasons: List[str] = []

    def _add(points: int, reason: str) -> None:
        nonlocal score
        if reason not in reasons:
            score += points
            reasons.append(reason)

    # --- Parse URL ---
    # If no scheme, prepend http:// so urlparse works
    parsed_url = url
    if not re.match(r"^https?://", url, re.IGNORECASE):
        parsed_url = "http://" + url

    try:
        parsed = urlparse(parsed_url)
    except Exception:
        _add(20, "Malformed URL structure")
        return {"score": min(score, 100), "reasons": reasons}

    hostname = parsed.hostname or ""
    path = unquote(parsed.path or "")
    query = unquote(parsed.query or "")
    full_lower = parsed_url.lower()

    # -----------------------------------------------------------------
    # 1. HTTP vs HTTPS
    # -----------------------------------------------------------------
    if parsed.scheme == "http":
        _add(15, "URL uses HTTP instead of HTTPS (no encryption)")

    # -----------------------------------------------------------------
    # 2. IP address instead of domain
    # -----------------------------------------------------------------
    if re.match(r"^\d{1,3}(\.\d{1,3}){3}$", hostname):
        _add(30, "URL uses an IP address instead of a domain name")
    elif re.match(r"^\[?[0-9a-fA-F:]+\]?$", hostname):
        # IPv6
        _add(30, "URL uses an IP address instead of a domain name")

    # -----------------------------------------------------------------
    # 3. Very long URL (> 75 characters)
    # -----------------------------------------------------------------
    if len(url) > 75:
        _add(10, "Unusually long URL")

    # -----------------------------------------------------------------
    # 4. @ symbol (can be used to obfuscate the real destination)
    # -----------------------------------------------------------------
    if "@" in parsed_url:
        _add(20, "URL contains '@' symbol which can hide the real destination")

    # -----------------------------------------------------------------
    # 5. Excessive dots in hostname (> 3)
    # -----------------------------------------------------------------
    dot_count = hostname.count(".")
    if dot_count > 3:
        _add(10, "Excessive dots in the hostname (possible subdomain abuse)")

    # -----------------------------------------------------------------
    # 6. Excessive hyphens in hostname (> 2)
    # -----------------------------------------------------------------
    hyphen_count = hostname.count("-")
    if hyphen_count > 2:
        _add(10, "Excessive hyphens in the hostname")

    # -----------------------------------------------------------------
    # 7. Excessive subdomains (> 3 parts before TLD)
    # -----------------------------------------------------------------
    parts = hostname.split(".")
    if len(parts) > 4:
        _add(15, "Excessive subdomains detected")

    # -----------------------------------------------------------------
    # 8. Suspicious URL encoding (lots of %xx sequences)
    # -----------------------------------------------------------------
    encoding_count = len(re.findall(r"%[0-9a-fA-F]{2}", url))
    if encoding_count > 3:
        _add(10, "Heavy URL-encoding may be hiding the true destination")

    # -----------------------------------------------------------------
    # 9. Suspicious keywords in URL
    # -----------------------------------------------------------------
    keyword_hits = [kw for kw in _SUSPICIOUS_KEYWORDS if kw in full_lower]
    if len(keyword_hits) >= 3:
        _add(20, "Multiple suspicious keywords in URL (e.g. login, verify, account)")
    elif len(keyword_hits) >= 1:
        _add(12, "Suspicious keyword found in URL")

    # -----------------------------------------------------------------
    # 10. URL shortener
    # -----------------------------------------------------------------
    if hostname.lower() in _SHORTENERS:
        _add(15, "URL uses a known URL shortener service")

    # -----------------------------------------------------------------
    # 11. Unusual port
    # -----------------------------------------------------------------
    if parsed.port and parsed.port not in (80, 443):
        _add(15, "URL uses an unusual port number")

    # -----------------------------------------------------------------
    # 12. Query-string complexity (many parameters)
    # -----------------------------------------------------------------
    if query:
        param_count = query.count("&") + 1
        if param_count > 5:
            _add(10, "Complex query string with many parameters")

    # -----------------------------------------------------------------
    # 13. Punycode / internationalized domain
    # -----------------------------------------------------------------
    if hostname.startswith("xn--") or any(
        part.startswith("xn--") for part in parts
    ):
        _add(15, "Domain uses Punycode (internationalized characters)")

    # -----------------------------------------------------------------
    # 14. Suspicious TLD patterns (double extensions, misleading)
    # -----------------------------------------------------------------
    if re.search(r"\.(tk|ml|ga|cf|gq|buzz|xyz|top|pw|cc|click)\b", hostname, re.IGNORECASE):
        _add(8, "Domain uses a TLD commonly associated with free/disposable domains")

    # -----------------------------------------------------------------
    # 15. Security-themed hostname (e.g. secure-login-verify.example.com)
    # -----------------------------------------------------------------
    hostname_keywords = [kw for kw in _SUSPICIOUS_KEYWORDS if kw in hostname.lower()]
    if len(hostname_keywords) >= 2:
        _add(15, "Domain name contains multiple security-related terms")

    # -----------------------------------------------------------------
    # 16. Credentials embedded in URL
    # -----------------------------------------------------------------
    if parsed.username or parsed.password:
        _add(25, "URL contains embedded credentials (e.g., user:pass@...)")

    # -----------------------------------------------------------------
    # 17. Suspicious Redirects
    # -----------------------------------------------------------------
    if re.search(r"(?i)(url|next|redirect|returnTo)=http", query) or "/http" in path.lower():
        _add(15, "URL contains open-redirect patterns")

    # -----------------------------------------------------------------
    # 18. Excessive Path Depth
    # -----------------------------------------------------------------
    if len([p for p in path.split("/") if p]) > 5:
        _add(10, "Unusually deep path structure")

    # -----------------------------------------------------------------
    # 19. Brand Impersonation
    # -----------------------------------------------------------------
    popular_brands = ["paypal", "microsoft", "apple", "google", "amazon", "facebook", "netflix", "chase", "bankofamerica"]
    for brand in popular_brands:
        if brand in full_lower:
            if brand in path.lower() or brand in query.lower():
                 _add(15, f"Popular brand ({brand}) found in URL path or query (impersonation risk)")
            elif brand in hostname and not (hostname.endswith(f"{brand}.com") or hostname.endswith(f"{brand}.net") or hostname.endswith(f"{brand}.org") or hostname == brand):
                 _add(20, f"Popular brand ({brand}) embedded in suspicious hostname")

    # Cap score at 100
    score = min(score, 100)

    return {"score": score, "reasons": reasons}
