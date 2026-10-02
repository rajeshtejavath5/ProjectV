from __future__ import annotations

import os
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("KGF_DATABASE", BASE_DIR / "data" / "enquiries.sqlite3"))
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

AREAS = ["Yadadri Bhuvanagiri", "Alair", "Gajwel", "Medchal", "Chakripur", "Tarnaka", "Nearby / other area"]


def connect_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.execute("""CREATE TABLE IF NOT EXISTS enquiries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT NOT NULL,
        customer_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        area TEXT NOT NULL,
        quantity TEXT NOT NULL,
        address TEXT NOT NULL,
        preferred_date TEXT,
        notes TEXT
    )""")
    return db


@app.get("/")
def home():
    return render_template("index.html", areas=AREAS)


@app.post("/api/enquiries")
def create_enquiry():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    phone = re.sub(r"[^\d+]", "", str(data.get("phone", "")))
    area = str(data.get("area", "")).strip()
    quantity = str(data.get("quantity", "")).strip()
    address = str(data.get("address", "")).strip()
    preferred_date = str(data.get("preferred_date", "")).strip()[:10]
    notes = str(data.get("notes", "")).strip()[:1000]
    if not all((name, phone, area, quantity, address)):
        return jsonify(error="Please complete all required fields."), 400
    if len(name) > 100 or len(phone) < 7 or len(phone) > 16 or len(quantity) > 80 or len(address) > 500:
        return jsonify(error="Please check the length and format of your details."), 400
    if area not in AREAS:
        return jsonify(error="Please choose a delivery area from the list."), 400
    with connect_db() as db:
        cur = db.execute("""INSERT INTO enquiries
            (created_at, customer_name, phone, area, quantity, address, preferred_date, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (datetime.now(timezone.utc).isoformat(), name, phone, area, quantity, address, preferred_date, notes))
        enquiry_id = cur.lastrowid
    return jsonify(id=enquiry_id, message="Enquiry saved on this server."), 201


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
