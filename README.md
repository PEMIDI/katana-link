# Katana Link 🔗

A tiny, clean URL shortener built with FastAPI. Paste a long link, get a short one, and redirect instantly. Minimal config. Maximum speed. ⚡


## Quickstart 🚀

Prerequisites
- Python 3.11+
- PostgreSQL (make sure the database exists)
- Optional: Redis (for visit counters)

1) Clone and set up
- git clone <your-fork-or-repo-url>
- cd katana-link/src
- python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
- pip install -r requirements.txt

2) Configure env
- cp .env.example .env
- Edit .env if needed. Example:
  - ENV=development
  - DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/katana
  - SHORT_DOMAIN=http://localhost:8000
  - ENABLE_DOCS=true
  - LOG_LEVEL=INFO

Notes
- In non-production, the app auto-creates tables on startup. In production, use Alembic.
- Ensure your PostgreSQL database (e.g., "katana") exists before running the app.

3) Run the API
- uvicorn app.app:app --reload
- Open docs: http://localhost:8000/docs
- Health check: GET http://localhost:8000/healthz


## How to use ✂️➡️
- Create short link
  - POST /short_url
  - JSON body: { "long_link": "https://example.com/path" }
  - Response: { "short_link": "http://localhost:8000/abc123", "long_link": "..." }
- Redirect
  - GET /{short_code} → 301 redirect to the original URL


## Testing ✅
- pytest -q


## Configuration ⚙️
Main env keys (see app/core/config.py)
- DATABASE_URL: PostgreSQL async DSN (default points to localhost)
- SHORT_DOMAIN: Public base used to build short links (default http://localhost:8000)
- ENV, ENABLE_DOCS, LOG_LEVEL, SQL_ECHO
Optional
- REDIS_HOST, REDIS_PORT (for visit counters in Redis)

Migrations (optional) 🗄️
- alembic -c app/alembic.ini upgrade head


## Publish on GitHub 🌐
If starting from a local folder:
- git init
- git add .
- git commit -m "Initial commit: Katana Link"
- Create a repo on GitHub (web UI or GitHub CLI)
- git remote add origin https://github.com/<you>/katana-link.git
- git push -u origin main  # or master


## Tech stack 🧰
- FastAPI + Starlette
- SQLAlchemy (async) + PostgreSQL
- Alembic (migrations)
- Redis (optional, for counters)

Enjoy! 🎉
