# ThreatLens

**AI-powered phishing detection with explainable risk analysis.**

---

## Problem

Phishing attacks remain one of the most common and effective cyber threats. Users often lack the tools or knowledge to quickly assess whether a message or URL is malicious before clicking.

## Solution

PhishGuard AI analyzes suspicious messages and URLs using deterministic rule-based analysis, calculates separate risk scores, combines them into an overall assessment, and explains exactly **why** something was flagged — empowering users to make informed decisions.

## Features

- **Message Analysis** — Detects urgency, credential requests, threats, impersonation, and more
- **URL Analysis** — Inspects structural features like IP addresses, suspicious keywords, encoding tricks, and shorteners
- **Combined Risk Scoring** — Weighted combination of message and URL risk scores
- **Explainable Results** — Every classification comes with clear, human-readable reasons
- **Three Classifications** — SAFE, SUSPICIOUS, or PHISHING with color-coded indicators
- **No External APIs Required** — Fully functional without paid services or API keys

## Architecture

```
User
 ↓
React Frontend (Vite + Tailwind)
 ↓
FastAPI Backend
 ├── Message Analyzer (rule-based NLP)
 └── URL Analyzer (structural analysis)
 ↓
Risk Engine
 ↓
Risk Classification
 ↓
Explainable Result
```

## Technology Stack

| Layer    | Technology                     |
|----------|-------------------------------|
| Frontend | React, Vite, Tailwind CSS     |
| Backend  | Python, FastAPI, Pydantic     |
| Server   | Uvicorn                       |
| Testing  | Pytest, FastAPI TestClient    |

## Folder Structure

```
ThreatLens/
├── frontend/
│   ├── src/
│   │   ├── components/   — UI components
│   │   ├── pages/        — Page layouts
│   │   ├── services/     — API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
│
├── backend/
│   ├── analyzers/
│   │   ├── message_analyzer.py
│   │   └── url_analyzer.py
│   ├── main.py           — FastAPI app
│   ├── models.py         — Pydantic schemas
│   ├── risk_engine.py    — Score combination
│   └── requirements.txt
│
├── tests/
│   ├── test_message_analyzer.py
│   ├── test_url_analyzer.py
│   └── test_api.py
│
├── API_CONTRACT.md
├── README.md
└── .gitignore
```

## Installation

### Backend

```bash
cd ThreatLens/backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
```

### Frontend

```bash
cd ThreatLens/frontend
npm install
```

## Running

### Backend

```bash
cd ThreatLens/backend
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.
Interactive docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd ThreatLens/frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## API Endpoint

### `POST /analyze`

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "URGENT! Verify your account immediately!",
    "url": "http://192.168.1.50/login/verify-account"
  }'
```

### Example Response

```json
{
    "classification": "PHISHING",
    "risk_score": 92,
    "message_score": 88,
    "url_score": 95,
    "reasons": [
        "Urgency language detected in message",
        "Account suspension or security threat language detected",
        "URL uses an IP address instead of a domain name",
        "URL uses HTTP instead of HTTPS"
    ]
}
```

## Testing

```bash
cd ThreatLens
python -m pytest tests/ -v
```

## Team Responsibilities

| Member   | Responsibility                        |
|----------|---------------------------------------|
| Member 1 | Frontend / UI                         |
| Member 2 | URL Analyzer (`url_analyzer.py`)      |
| Member 3 | Message Analyzer (`message_analyzer.py`) |
| Member 4 | FastAPI Backend + Integration         |

See [API_CONTRACT.md](API_CONTRACT.md) for the integration contract.

## License

Hackathon project — for educational and demonstration purposes.
