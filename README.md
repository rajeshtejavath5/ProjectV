# KGF Bricks Suppliers

A mobile-first Flask website with a WhatsApp enquiry flow and SQLite enquiry record.

## Run locally

1. Install Python 3.10+.
2. From this folder, run `python -m venv .venv`.
3. Activate it (`.venv\Scripts\Activate.ps1` on Windows, or `source .venv/bin/activate` on macOS/Linux).
4. Run `pip install -r requirements.txt`.
5. Run `python app.py` and open http://127.0.0.1:5000.

Enquiries are stored in `data/enquiries.sqlite3` on the server, then the browser opens a pre-filled WhatsApp message to 9603804243. Customers must press Send in WhatsApp. There is no admin dashboard or order confirmation workflow. Store the database securely and configure backups before using this as a public production service. For a free static host such as GitHub Pages, this Python-backed version must be adapted to a static form that only prepares the WhatsApp message.

The hero delivery lorry and red brick product imagery are local WebP assets in `static/assets`, so they load without relying on remote stock-photo services. External Google Fonts are optional; the page falls back to system fonts.
