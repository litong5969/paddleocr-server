# Changelog

## v0.2.0 — 2025-12-08

Highlights
- Lightweight Web GUI integrated at `/ui` (same container/port as API)
- Full-screen Screenshot → Preview → Confirm → OCR (HTTPS/localhost)
- HTTP intranet fallback preserved; print fallback kept for non-supported cases
- Optional TLS in the same port via `SSL_CERTFILE`/`SSL_KEYFILE`
- Local gates: `make selfcheck` / `make test` / `make perf-baseline`

Details
- feat(gui): single-page HTML/JS; drag/drop or select images; results + scores
- feat(shot): full-screen capture with preview; on confirm posts to `POST /ocr`
- feat(server): optional TLS; `/` redirects to `/ui`; static mount for GUI
- chore(compose): mount `./web:/app/web:ro`; override example for TLS; `HOST_PORT=5215`
- docs: README GUI + TLS how-to; PM bootstrap; roadmap; kanban

Upgrade Notes
- API unchanged; GUI added at `/ui` and shares port `5215`
- To enable full-screen capture, access via HTTPS or localhost

Commits
- See `git log` around tag v0.2.0 for full history.

