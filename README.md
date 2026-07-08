# QR Code API

Generate customizable QR codes with FastAPI. Supports custom colors, embedded logos, SVG/PNG output, and bulk generation. Built for RapidAPI monetization.

## Quick Start

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| POST | `/v1/generate` | Generate a single QR code |
| POST | `/v1/generate/bulk` | Generate up to 100 QR codes |
| GET | `/v1/health` | Health check |

## API Docs

- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`

## Deploy

```bash
# Render (one-click)
# Push to GitHub → Connect to Render → Blueprint deploy
```

## License

MIT
