from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import secrets
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

DB = "linkpulse.db"


# Connect to SQLite
def connect_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


# Create the database table
def init_db():
    with connect_db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                original_url TEXT NOT NULL,
                clicks INTEGER DEFAULT 0
            )
        """)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Create a short link
@app.route("/create", methods=["POST"])
def create():
    original_url = request.form.get("url", "").strip()

    # Check that the URL is valid
    parsed = urlparse(original_url)

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        flash("Please enter a valid URL starting with http:// or https://")
        return redirect(url_for("home"))

    # Generate a unique short code
    with connect_db() as con:
        while True:
            code = secrets.token_urlsafe(5)[:7]
            exists = con.execute(
                "SELECT 1 FROM links WHERE code = ?", (code,)
            ).fetchone()

            if not exists:
                break

        con.execute(
            "INSERT INTO links (code, original_url) VALUES (?, ?)",
            (code, original_url)
        )

    short_url = request.host_url + code
    return render_template(
        "index.html",
        short_url=short_url,
        original_url=original_url
    )


# Show saved links and click counts
@app.route("/links")
def links():
    with connect_db() as con:
        all_links = con.execute(
            "SELECT * FROM links ORDER BY id DESC"
        ).fetchall()

    return render_template("links.html", links=all_links)


# Redirect visitors to the original URL
@app.route("/<code>")
def go(code):
    with connect_db() as con:
        link = con.execute(
            "SELECT * FROM links WHERE code = ?", (code,)
        ).fetchone()

        if link is None:
            return "Short link not found", 404

        con.execute(
            "UPDATE links SET clicks = clicks + 1 WHERE code = ?",
            (code,)
        )

    return redirect(link["original_url"])


# Start the application
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
