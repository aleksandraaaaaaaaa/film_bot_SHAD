import sqlite3

DB_PATH = "bot.db"


def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS queries (
            user_id INTEGER,
            query TEXT,
            movie_title TEXT
        );
        """)


def save_query(user_id, query, title):
    with sqlite3.connect(DB_PATH) as con:
        con.execute("INSERT INTO queries (user_id, query, movie_title) VALUES (?, ?, ?)", (user_id, query, title))


def get_history(user_id):
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.execute("SELECT query FROM queries WHERE user_id = ?", (user_id,))
        return [row[0] for row in cursor.fetchall()]


def get_stats(user_id):
    with sqlite3.connect(DB_PATH) as con:
        cursor = con.execute("SELECT movie_title, COUNT(*) FROM queries WHERE user_id = ? GROUP BY movie_title",
                             (user_id,))
        return {row[0]: row[1] for row in cursor.fetchall()}
