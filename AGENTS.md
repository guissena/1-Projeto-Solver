# Base44 Dev Environment

## Project Overview
This is a Python/Flask web app wrapping a credit card interest calculator and flowchart generator (originally a CLI script in README.md). It uses the `graphviz` library to generate SVG flowcharts.

## Setup
- Run: `docker compose -f docker-compose.base44.yml up -d --build`
- App is served on port 3000 (Flask dev server, debug mode)
- No external secrets or credentials required
- Source is bind-mounted; Flask debug reloader picks up edits automatically

## Key Files
- `app.py` — Flask app with embedded HTML template (form + results + SVG flowchart)
- `requirements.txt` — flask, graphviz
- `Dockerfile` — python:3.12-slim + system graphviz package
- `docker-compose.base44.yml` — compose setup

## How to Verify
- GET `/` shows the input form
- POST with `compras` (comma-separated values), `fechamento` (date), `pagamento` (date) returns calculated interest + SVG flowchart
- Payment day ≤ 25: no interest; day > 25: interest = total × (0.03 + (day−25) × 0.01)
