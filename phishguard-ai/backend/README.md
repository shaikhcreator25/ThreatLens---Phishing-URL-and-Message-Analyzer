# PhishGuard AI — Backend

FastAPI backend for PhishGuard AI phishing detection.

## Quick Start

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Endpoints

| Method | Path       | Description                     |
|--------|------------|---------------------------------|
| GET    | `/health`  | Liveness probe                  |
| POST   | `/analyze` | Analyze message and/or URL      |
| GET    | `/docs`    | Interactive Swagger UI          |

## Architecture

```
main.py            → FastAPI app, routing, CORS
models.py          → Pydantic request/response schemas
risk_engine.py     → Score combination & classification
analyzers/
  message_analyzer.py → Rule-based message analysis
  url_analyzer.py     → Rule-based URL analysis
```
