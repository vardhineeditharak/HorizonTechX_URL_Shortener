# Shrnk URL Shortener

Simple Flask-based URL shortener.

## Features

- Shortens long URLs
- Stores links in SQLite
- Redirects short links to the original URL

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   python app.py
   ```

4. Open `http://127.0.0.1:5000` in your browser.

## Notes

- `urls.db` is created automatically when the app starts.
- `venv/` and other local files are ignored by Git.