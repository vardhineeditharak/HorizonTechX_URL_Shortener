from flask import Flask, request, redirect, render_template, jsonify
import os
import sqlite3
import string
import random

app = Flask(__name__)

SHORT_URL_PREFIX = "Shrnk"
SHORT_URL_BASE = os.environ.get("SHORT_URL_BASE")


def build_short_url(short_code):
    base_url = SHORT_URL_BASE or request.host_url.rstrip('/')
    return base_url.rstrip('/') + '/' + SHORT_URL_PREFIX + '/' + short_code

# ---------- DATABASE ----------

def init_db():
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT NOT NULL UNIQUE
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------- SHORT CODE GENERATOR ----------

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    while True:
        short_code = ''.join(random.choice(characters) for _ in range(length))

        conn = sqlite3.connect('urls.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM urls WHERE short_code=?",
            (short_code,)
        )

        exists = cursor.fetchone()

        conn.close()

        if not exists:
            return short_code

# ---------- HOME PAGE ----------

@app.route('/')
def home():
    return render_template('index.html')

# ---------- API TO SHORTEN URL ----------

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.form

    original_url = data.get('url')

    if not original_url:
        return render_template(
            'index.html',
            error="URL is required."
        )

    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    short_code = generate_short_code()

    # ---------- SAVE TO DATABASE ----------

    cursor.execute(
        "INSERT INTO urls (original_url, short_code) VALUES (?, ?)",
        (original_url, short_code)
    )

    conn.commit()
    conn.close()

    short_url = build_short_url(short_code)

    return render_template(
        'index.html',
        short_url=short_url
    )

# ---------- REDIRECT ROUTE ----------

@app.route(f'/{SHORT_URL_PREFIX}<short_code>')
def redirect_to_url(short_code):
    conn = sqlite3.connect('urls.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT original_url FROM urls WHERE short_code=?",
        (short_code,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:
        return redirect(result[0])

    return "URL not found", 404

# ---------- RUN SERVER ----------

if __name__ == '__main__':
    app.run(debug=True)