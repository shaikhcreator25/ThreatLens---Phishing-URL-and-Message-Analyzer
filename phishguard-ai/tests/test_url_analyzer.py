"""Tests for the URL analyzer."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from analyzers.url_analyzer import analyze_url


class TestUrlAnalyzer:
    """Tests for analyze_url()."""

    def test_safe_url(self):
        result = analyze_url("https://www.google.com")
        assert result["score"] < 40
        assert isinstance(result["reasons"], list)

    def test_suspicious_url_keywords(self):
        result = analyze_url("http://secure-account-verification.example.com/login")
        assert result["score"] > 0
        assert len(result["reasons"]) > 0

    def test_ip_based_url(self):
        result = analyze_url("http://192.168.1.50/login/verify-account")
        assert result["score"] >= 25
        assert any("IP address" in r for r in result["reasons"])

    def test_url_with_at_symbol(self):
        result = analyze_url("http://google.com@evil.com/phishing")
        assert result["score"] >= 20
        assert any("@" in r for r in result["reasons"])

    def test_long_url(self):
        result = analyze_url("https://example.com/" + "a" * 100)
        assert any("long" in r.lower() for r in result["reasons"])

    def test_http_no_https(self):
        result = analyze_url("http://example.com")
        assert any("HTTP" in r for r in result["reasons"])

    def test_url_shortener(self):
        result = analyze_url("https://bit.ly/abc123")
        assert any("shortener" in r.lower() for r in result["reasons"])

    def test_unusual_port(self):
        result = analyze_url("https://example.com:8443/login")
        assert any("port" in r.lower() for r in result["reasons"])

    def test_empty_url(self):
        result = analyze_url("")
        assert result["score"] == 0
        assert result["reasons"] == []

    def test_none_url(self):
        result = analyze_url(None)
        assert result["score"] == 0
        assert result["reasons"] == []

    def test_excessive_subdomains(self):
        result = analyze_url("http://a.b.c.d.e.example.com/login")
        assert any("subdomain" in r.lower() for r in result["reasons"])

    def test_punycode_domain(self):
        result = analyze_url("http://xn--80ak6aa92e.com/login")
        assert any("punycode" in r.lower() or "internationalized" in r.lower() for r in result["reasons"])

    def test_credentials_in_url(self):
        result = analyze_url("https://admin:password123@example.com")
        assert any("credentials" in r.lower() for r in result["reasons"])

    def test_suspicious_redirects(self):
        result = analyze_url("https://example.com/login?next=http://evil.com")
        assert any("redirect" in r.lower() for r in result["reasons"])

    def test_excessive_path_depth(self):
        result = analyze_url("https://example.com/a/b/c/d/e/f/g/h")
        assert any("deep path" in r.lower() for r in result["reasons"])

    def test_brand_impersonation(self):
        result = analyze_url("https://paypal-update.secure-login.com")
        assert any("impersonation" in r.lower() or "brand" in r.lower() for r in result["reasons"])

    def test_score_capped_at_100(self):
        result = analyze_url(
            "http://192.168.1.1:9999@evil.com/login/verify/account/secure/"
            + "x" * 100
            + "?a=1&b=2&c=3&d=4&e=5&f=6"
        )
        assert result["score"] <= 100
