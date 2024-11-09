import logging
import os
import sqlite3
import math
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, request, abort, g

load_dotenv()
DATABASE = os.getenv("TASKS_DATABASE_URL").replace("sqlite:///", "")
LOG_FILE = os.getenv("TASKS_LOG_FILE")
APP_HOST = os.getenv("APP_HOST")
APP_PORT = 5000
APP_DEBUG = os.getenv("APP_DEBUG") == "True"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)


def is_date_and_in_past(date_as_text: None | str):
    if date_as_text is None:
        return False
    try:
        date = datetime.strptime(date_as_text, "%Y-%m-%d")  # Adjust format as needed
        return date < datetime.now()
    except ValueError:
        return False


def worth(priority: int, difficulty: int, due_date: None | str) -> int:
    score = priority * difficulty * 10
    if is_date_and_in_past(due_date):
        return math.floor(score / 2)
    return score


def get_existing_or_create_db():
    db = getattr(g, "_database", None)
    if db is None:
        # Habituellement, un DATABASE_URL est un _dsn_ et est parsé, puis le bon connecteur est utilisé
        # Ici, nous allons juste partir du principe que la valeur attendue est de la forme sqlite:////path/to/file
        logger.info(f"Connecting to the database: {DATABASE}")
        db = g._database = sqlite3.connect(
            DATABASE.replace("sqlite:///", ""),
        )
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    with app.app_context():
        db = get_existing_or_create_db()
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL CHECK (completed IN (0,1)) DEFAULT 0,
                due_date TEXT,
                priority INTEGER DEFAULT 1,
                difficulty INTEGER DEFAULT 1
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_score INTEGER NOT NULL DEFAULT 0
            )
        """)
        db.commit()


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "title" not in data:
        abort(400, "Le titre est obligatoire pour ajouter une tâche.")

    db = get_existing_or_create_db()
    cursor = db.cursor()

    priority = data.get("priority", 1)
    difficulty = data.get("difficulty", 1)

    due_date = data.get("due_date", None)
    cursor.execute(
        """
        INSERT INTO tasks (title, description, due_date, priority, difficulty)
        VALUES (?, ?, ?, ?, ?)
    """,
        (
            data["title"],
            data.get("description"),
            due_date,
            priority,
            difficulty,
        ),
    )
    db.commit()
    task_id = cursor.lastrowid
    logger.info(
        f"Tâche ajoutée avec ID {task_id} et date d'échéance {data.get('due_date')}"
    )
    return jsonify(
        {
            "id": task_id,
            "title": data["title"],
            "description": data.get("description"),
            "priority": priority,
            "difficulty": difficulty,
            "due_date": due_date,
            "worth": worth(priority, difficulty, due_date),
        }
    ), 201


@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
def complete_task(task_id):
    db = get_existing_or_create_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT priority, difficulty, completed, due_date FROM tasks WHERE id = ?",
        (task_id,),
    )
    task = cursor.fetchone()

    if task is None:
        abort(404, "Tâche non trouvée.")

    print(task)
    if task["completed"] == 1:
        abort(400, "Tâche déjà complétée.")

    score = worth(
        priority=task["priority"],
        difficulty=task["difficulty"],
        due_date=task["due_date"],
    )

    cursor.execute("INSERT OR IGNORE INTO scores (total_score) VALUES (?)", (score,))
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    db.commit()
    logger.info(f"Tâche {task_id} marquée comme terminée avec un score de {score}.")
    return jsonify(
        {"message": "Tâche marquée comme terminée", "score_added": score}
    ), 200


@app.route("/tasks/cleanup", methods=["DELETE"])
def cleanup_tasks():
    db = get_existing_or_create_db()
    cursor = db.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("DELETE FROM tasks WHERE completed = 1 OR due_date < ?", (today,))
    deleted_count = cursor.rowcount
    db.commit()
    logger.info(f"Nettoyage terminé : {deleted_count} tâches supprimées.")
    return jsonify(
        {"message": f"{deleted_count} tâches obsolètes ou complétées supprimées"}
    ), 200


@app.route("/scores/total", methods=["GET"])
def get_total_score():
    db = get_existing_or_create_db()
    cursor = db.cursor()
    cursor.execute("SELECT SUM(total_score) as total_score FROM scores")
    row = cursor.fetchone()
    return jsonify({"total_score": row["total_score"]}), 200


@app.route("/tasks/active", methods=["GET"])
def get_active_tasks():
    db = get_existing_or_create_db()
    cursor = db.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    cursor.execute(
        "SELECT * FROM tasks WHERE completed = 0 AND (due_date >= ? OR due_date IS NULL)",
        (today,),
    )
    tasks = cursor.fetchall()

    if not tasks:
        return jsonify({"message": "Aucune tâche active trouvée."}), 404

    result = [
        {
            "id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "completed": task["completed"],
            "due_date": task["due_date"],
            "priority": task["priority"],
            "difficulty": task["difficulty"],
            "worth": worth(
                priority=task["priority"],
                difficulty=task["difficulty"],
                due_date=task["due_date"],
            ),
        }
        for task in tasks
    ]
    return jsonify(result), 200


if __name__ == "__main__":
    init_db()
    app.run(host=APP_HOST, port=APP_PORT, debug=APP_DEBUG)
