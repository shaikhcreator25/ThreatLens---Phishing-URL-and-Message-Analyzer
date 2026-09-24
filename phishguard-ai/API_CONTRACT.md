# PhishGuard AI API Contract

> **This document is the integration contract for the 4-person team.**
> Do not change field names without documenting the change here.

---

## `POST /analyze`

Analyze a suspicious message and/or URL for phishing indicators.

### Request

```json
{
    "message": "string (optional)",
    "url": "string (optional)"
}
```

| Field     | Type   | Required | Description                       |
|-----------|--------|----------|-----------------------------------|
| `message` | string | No*      | Suspicious message text           |
| `url`     | string | No*      | Suspicious URL to analyze         |

*At least one of `message` or `url` must be provided. Empty strings are treated as missing.

### Response

```json
{
    "classification": "PHISHING",
    "risk_score": 92,
    "message_score": 88,
    "url_score": 95,
    "reasons": [
        "Urgency language detected in message",
        "Account suspension or security threat language detected",
        "URL uses an IP address instead of a domain name"
    ]
}
```

| Field            | Type     | Description                                           |
|------------------|----------|-------------------------------------------------------|
| `classification` | string   | `"SAFE"`, `"SUSPICIOUS"`, or `"PHISHING"`             |
| `risk_score`     | integer  | Overall risk score (0–100)                            |
| `message_score`  | integer  | Message analysis score (0–100), 0 if no message       |
| `url_score`      | integer  | URL analysis score (0–100), 0 if no URL               |
| `reasons`        | string[] | Human-readable explanations (max 7 items)             |

### Classification Thresholds

| Score Range | Classification |
|-------------|----------------|
| 0–34        | SAFE           |
| 35–69       | SUSPICIOUS     |
| 70–100      | PHISHING       |

### Score Calculation

When both message and URL are provided:

```
risk_score = message_score × 0.45 + url_score × 0.55
```

When only one input is provided, its score is used directly as the risk score.

---

## `GET /health`

Liveness probe.

### Response

```json
{
    "status": "ok"
}
```

---

## Error Responses

### 422 — Validation Error

Returned when both `message` and `url` are missing or empty.

```json
{
    "detail": "At least one of 'message' or 'url' must be provided."
}
```

---

## Example Requests

### Phishing (both inputs)

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "URGENT! Your bank account will be suspended today. Verify immediately!",
    "url": "http://192.168.1.50/login/verify-account"
  }'
```

### Message only

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "Enter your OTP to confirm the transaction."}'
```

### URL only

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "http://bit.ly/suspicious-link"}'
```

### Safe message

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "Hey, are we still meeting at 5 PM today?"}'
```
