# librairie.py
import os
import sqlite3
import logging
from flask import Flask, jsonify, request, abort, g
from dotenv import load_dotenv

# Dotenv permet de charger les variables d'environnement depuis un fichier .env
# De sorte à rendre le développement plus facile
load_dotenv()

app = Flask(__name__)
DATABASE = os.getenv("LIBRARY_DATABASE_URL")
LOG_FILE = os.getenv("LIBRARY_LOG_FILE")
APP_HOST = os.getenv("APP_HOST")
APP_DEBUG = os.getenv("APP_DEBUG") == "True"
APP_PORT = 5000

# Configurer le logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def get_existing_or_create_db():
    db = getattr(g, "database", None)
    if db is None:
        # Habituellement, un DATABASE_URL est un _dsn_ et est parsé, puis le bon connecteur est utilisé
        # Ici, nous allons juste partir du principe que la valeur attendue est de la forme sqlite:////path/to/file
        logger.info(f"Connecting to the database: {DATABASE}")
        db = g.database = sqlite3.connect(DATABASE.replace("sqlite:///", ""))
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "database", None)
    if db is not None:
        logger.info("Closing the database connection.")
        db.close()


def init_db():  # pragma: no cover
    with app.app_context():
        db = get_existing_or_create_db()
        cursor = db.cursor()
        logger.info("Initializing the database.")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                stock INTEGER DEFAULT 1
            )
        """)
        db.commit()


# Routes


@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    if not data or "title" not in data or "author" not in data or "stock" not in data:
        logger.error("Failed to add book: missing title, author, or stock.")
        abort(400, "Le titre, l'auteur et le stock sont obligatoires.")

    logger.info(
        f"Adding book with title '{data['title']}' by '{data['author']}' with stock {data['stock']}."
    )
    db = get_existing_or_create_db()
    cursor = db.cursor()
    cursor.execute(
        """
        INSERT INTO books (title, author, year, stock) VALUES (?, ?, ?, ?)
    """,
        (data["title"], data["author"], data.get("year"), data["stock"]),
    )
    db.commit()
    book_id = cursor.lastrowid
    book = {
        "id": book_id,
        "title": data["title"],
        "author": data["author"],
        "year": data.get("year"),
        "stock": data["stock"],
    }
    return jsonify(book), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    if not data or "title" not in data or "author" not in data or "stock" not in data:
        logger.error("Failed to update book: missing title, author, or stock.")
        abort(400, "Le titre, l'auteur et le stock sont obligatoires.")

    logger.info(
        f"Updating book with title '{data['title']}' by '{data['author']}' with stock {data['stock']}."
    )
    db = get_existing_or_create_db()
    cursor = db.cursor()
    cursor.execute(
        """
        REPLACE INTO books (id, title, author, year, stock) VALUES (?, ?, ?, ?, ?)
    """,
        (book_id, data["title"], data["author"], data.get("year"), data["stock"]),
    )
    db.commit()
    book = {
        "id": book_id,
        "title": data["title"],
        "author": data["author"],
        "year": data.get("year"),
        "stock": data["stock"],
    }
    return jsonify(book), 201


@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    logger.info(f"Retrieving book with ID {book_id}.")
    db = get_existing_or_create_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if book is None:
        logger.warning(f"Book with ID {book_id} not found.")
        abort(404, "Livre non trouvé.")
    return jsonify(
        {
            "id": book[0],
            "title": book[1],
            "author": book[2],
            "year": book[3],
            "stock": book[4],
        }
    )


# Ajout d'une route pour rechercher des livres
@app.route("/books/search/<value>", methods=["GET"])
def search_books(value):
    logger.info(f"Searching for books with keyword '{value}'.")
    db = get_existing_or_create_db()
    cursor = db.cursor()
    # Rechercher les livres où le mot-clé correspond au titre ou à l'auteur
    cursor.execute(
        """
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ?
    """,
        (f"%{value}%", f"%{value}%"),
    )
    books = cursor.fetchall()

    if not books:
        logger.info(f"No books found with keyword '{value}'.")
        return jsonify({"message": "Aucun livre trouvé."}), 404

    # Formater les résultats pour l'envoi en JSON
    result = [{"id": book[0], "title": book[1], "author": book[2]} for book in books]
    return jsonify(result), 200


@app.route("/books/<int:book_id>/borrow", methods=["POST"])
def borrow_book(book_id):
    logger.info(f"Borrowing book with ID {book_id}.")
    db = get_existing_or_create_db()
    cursor = db.cursor()
    cursor.execute("SELECT stock FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if book is None:
        logger.warning(f"Book with ID {book_id} not found for borrowing.")
        abort(404, "Livre non trouvé.")

    stock = book[0]
    if stock > 0:
        cursor.execute("UPDATE books SET stock = stock - 1 WHERE id = ?", (book_id,))
        db.commit()
        logger.info(f"Book with ID {book_id} borrowed successfully.")
        return jsonify({"message": "Livre emprunté avec succès"}), 200
    else:
        logger.warning(f"No stock available for book ID {book_id}.")
        abort(400, "Livre indisponible.")


@app.route("/books/<int:book_id>/return", methods=["POST"])
def return_book(book_id):
    logger.info(f"Returning book with ID {book_id}.")
    db = get_existing_or_create_db()
    cursor = db.cursor()
    cursor.execute("SELECT stock FROM books WHERE id = ?", (book_id,))
    book = cursor.fetchone()
    if book is None:
        logger.warning(f"Book with ID {book_id} not found for returning.")
        abort(404, "Livre non trouvé.")

    cursor.execute("UPDATE books SET stock = stock + 1 WHERE id = ?", (book_id,))
    db.commit()
    logger.info(f"Book with ID {book_id} returned successfully.")
    return jsonify({"message": "Livre retourné avec succès"}), 201


if __name__ == "__main__":  # pragma: no cover
    init_db()
    logger.info("Starting the Flask application.")
    app.run(debug=APP_DEBUG, host=APP_HOST, port=APP_PORT)
