
import sqlite3

DATABASE = "history.db"


def create_table():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            analysis_type TEXT NOT NULL,
            input_text TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    columns = [
        row[1]
        for row in connection.execute("PRAGMA table_info(analysis_history)")
    ]
    if "user_id" not in columns:
        connection.execute(
            "ALTER TABLE analysis_history ADD COLUMN user_id INTEGER"
        )

    connection.commit()
    connection.close()


def create_user(username, password_hash):
    connection = sqlite3.connect(DATABASE)

    try:
        cursor = connection.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )

        if cursor.lastrowid == 1:
            connection.execute(
                "UPDATE analysis_history SET user_id = ? WHERE user_id IS NULL",
                (cursor.lastrowid,)
            )

        connection.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None
    finally:
        connection.close()


def get_user(username):
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    user = connection.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    connection.close()
    return user


def save_analysis(user_id, analysis_type, input_text, result):
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        INSERT INTO analysis_history
        (user_id, analysis_type, input_text, result)
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        analysis_type,
        input_text,
        str(result)
    ))

    connection.commit()
    connection.close()


def get_history(user_id):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.execute("""
        SELECT id, analysis_type, input_text, result, created_at
        FROM analysis_history
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    records = cursor.fetchall()
    connection.close()

    return records