"""Tests for the Threat Intelligence module."""

import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from analyzers.threat_intel import check_url_reputation

class TestThreatIntel:
    """Tests for check_url_reputation()."""

    def test_no_api_key(self):
        with patch.dict(os.environ, clear=True):
            result = check_url_reputation("http://example.com")
            assert not result["known_malicious"]
            assert result["source"] == "local"

    @patch("urllib.request.urlopen")
    def test_malicious_url(self, mock_urlopen):
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"data": {"attributes": {"last_analysis_stats": {"malicious": 5, "suspicious": 1}}}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        with patch.dict(os.environ, {"THREAT_INTEL_API_KEY": "test_key"}):
            result = check_url_reputation("http://evil.com")
            assert result["known_malicious"] is True
            assert result["source"] == "virustotal"
            assert "malicious" in result["reason"]

    @patch("urllib.request.urlopen")
    def test_safe_url(self, mock_urlopen):
        # Mock HTTP response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.read.return_value = b'{"data": {"attributes": {"last_analysis_stats": {"malicious": 0, "suspicious": 0}}}}'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        with patch.dict(os.environ, {"THREAT_INTEL_API_KEY": "test_key"}):
            result = check_url_reputation("http://example.com")
            assert result["known_malicious"] is False
            assert result["source"] == "virustotal"
