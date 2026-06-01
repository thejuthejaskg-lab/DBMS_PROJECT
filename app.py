from flask import Flask, render_template, request, jsonify
import csv
import os
import sqlite3

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "library.db")
CSV_FILE = os.path.join(BASE_DIR, "book.csv")


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)
    conn.commit()

    if os.path.exists(CSV_FILE):
        cursor.execute("SELECT COUNT(*) FROM books")
        if cursor.fetchone()[0] == 0:
            with open(CSV_FILE, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if len(row) >= 3 and row[0].strip():
                        cursor.execute(
                            "INSERT OR IGNORE INTO books (id, title, author) VALUES (?, ?, ?)",
                            (row[0].strip(), row[1].strip(), row[2].strip())
                        )
            conn.commit()
    conn.close()


init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_book():
    data = request.json
    book_id = data.get("id", "").strip()
    title = data.get("title", "").strip()
    author = data.get("author", "").strip()

    if not book_id or not title or not author:
        return jsonify({"status": "Invalid book details"})

    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO books (id, title, author) VALUES (?, ?, ?)",
            (book_id, title, author)
        )
        conn.commit()
        conn.close()
        return jsonify({"status": "Book added"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "Book ID already exists"})
    except Exception as e:
        return jsonify({"status": f"Error: {str(e)}"})

@app.route("/get/<book_id>")
def get_book(book_id):
    book_id = book_id.strip()
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author FROM books WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return jsonify({"id": row[0], "title": row[1], "author": row[2]})
        return jsonify({"status": "not found"})
    except Exception as e:
        return jsonify({"status": f"Error: {str(e)}"})

@app.route("/delete", methods=["POST"])
def delete_book():
    book_id = request.json.get("id", "").strip()
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "Book deleted"})
    except Exception as e:
        return jsonify({"status": f"Error: {str(e)}"})

@app.route("/list")
def list_books():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author FROM books")
        rows = cursor.fetchall()
        conn.close()

        books = []
        for row in rows:
            books.append({
                "id": row[0],
                "title": row[1],
                "author": row[2]
            })
        return jsonify(books)
    except Exception as e:
        return jsonify({"status": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)