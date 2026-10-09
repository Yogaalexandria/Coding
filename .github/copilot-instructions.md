# Copilot instructions

## Project overview
- This is a small Indonesian fruit-shop demo: a Flask app serves `main.html`, and the page sends checkout requests back to the Flask app.
- `main.py` is the source of truth for product prices, quantity validation, subtotal, and the 10% discount (subtotal at least Rp50.000).
- `main.html` contains the static UI, browser-side formatting, and `fetch('/checkout')` integration. Keep the request/response fields aligned with the Flask route.

## Data flow and key files
- `GET /` in `main.py` serves `main.html`; `GET /health` returns a simple health response.
- `POST /checkout` accepts JSON quantities for `apel`, `jeruk`, and `pisang`, calls `calculate_order`, and returns JSON with `items`, `subtotal`, `discount`, `total`, and `discount_applied`. Validation failures return HTTP 400 with a `message`.
- `calculate_order` is shared by the web route and the CLI flow. Update it rather than duplicating pricing or discount rules in either interface.
- `main.html` formats returned amounts as Indonesian rupiah and displays success or error messages. Its checkout expects the Flask server and same-origin `/checkout` endpoint.

## Development workflow
- Start the app from the repository root with `python main.py`, then open `http://127.0.0.1:5000`.
- Flask is imported directly by `main.py`; there is no dependency manifest or test suite in the repository currently.
- `run_cli()` in `main.py` is an alternate interactive flow, but the script entry point starts Flask. Keep user-facing text in Indonesian and consistent with existing prompts/messages.
- For checkout changes, verify the threshold boundary (Rp50.000), totals, invalid/negative quantities, and the browser's handling of failed or invalid JSON responses.

## Conventions and scope
- Keep this educational demo direct and compact; follow the existing procedural style and avoid adding framework layers or dependencies without a clear requirement.
- Preserve the existing `/checkout` JSON field names and HTTP behavior unless changing the frontend and backend together.
- `main.html` is served by Flask; it is not a separate backend or Python integration layer. Avoid changing the app into a different architecture without an explicit request.
