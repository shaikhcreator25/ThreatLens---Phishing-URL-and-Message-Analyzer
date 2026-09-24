"""
PhishGuard AI — Threat Intelligence Module

Optional module to query a URL reputation service.
By default, this expects a VirusTotal API key in THREAT_INTEL_API_KEY.
"""

import os
import urllib.request
import json
import base64
from typing import Dict, Any

def check_url_reputation(url: str) -> Dict[str, Any]:
    """Check a URL against a threat intelligence service.

    Args:
        url: The URL to check.

    Returns:
        dict:
            known_malicious (bool): True if the service flags it.
            source (str): Source of the intel (e.g., 'virustotal', 'local').
            reason (str): Details about the detection.
    """
    api_key = os.environ.get("THREAT_INTEL_API_KEY")
    if not api_key:
        return {
            "known_malicious": False,
            "source": "local",
            "reason": "No API key configured for threat intel."
        }

    # VirusTotal v3 URL API expects the URL to be base64-encoded without padding.
    # We will safely attempt the request and fallback if it fails (timeout, 401, etc.)
    try:
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        vt_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        
        req = urllib.request.Request(vt_url)
        req.add_header("x-apikey", api_key)
        
        # Short timeout so we don't block the API for too long
        with urllib.request.urlopen(req, timeout=3.0) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                attributes = data.get("data", {}).get("attributes", {})
                last_analysis_stats = attributes.get("last_analysis_stats", {})
                
                malicious = last_analysis_stats.get("malicious", 0)
                suspicious = last_analysis_stats.get("suspicious", 0)
                
                if malicious > 0 or suspicious > 2:
                    return {
                        "known_malicious": True,
                        "source": "virustotal",
                        "reason": f"Flagged by {malicious} security vendors as malicious and {suspicious} as suspicious."
                    }
                else:
                    return {
                        "known_malicious": False,
                        "source": "virustotal",
                        "reason": "No malicious indicators found on VirusTotal."
                    }
                    
    except urllib.error.HTTPError as e:
        if e.code == 404:
            # URL not found in VT database, not necessarily malicious
            return {
                "known_malicious": False,
                "source": "virustotal",
                "reason": "URL not found in threat intel database."
            }
        return {
            "known_malicious": False,
            "source": "error",
            "reason": f"Threat intel service returned HTTP {e.code}"
        }
    except Exception as e:
        return {
            "known_malicious": False,
            "source": "error",
            "reason": f"Threat intel service error: {str(e)}"
        }

    return {
        "known_malicious": False,
        "source": "local",
        "reason": "Default fallback."
    }
