# PhishGuard AI — Frontend

React + Vite + Tailwind CSS frontend for PhishGuard AI.

## Quick Start

```bash
cd frontend
npm install
npm run dev
```

The app will be available at `http://localhost:5173`.

## Environment

Create a `.env` file:

```
VITE_API_URL=http://localhost:8000
```

## Structure

```
src/
├── components/
│   ├── Header.jsx           — Branding & tagline
│   ├── InputSection.jsx     — Message/URL inputs & demo buttons
│   ├── ResultDashboard.jsx  — Risk scores & classification
│   ├── ReasonsSection.jsx   — "Why was this flagged?"
│   └── Recommendation.jsx   — Safety advice
├── pages/
│   └── Dashboard.jsx        — Main page layout
├── services/
│   └── api.js               — Backend API client
├── App.jsx
├── main.jsx
└── index.css
```
