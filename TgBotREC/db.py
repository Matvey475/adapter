import sqlite3
from pathlib import Path

DB_PATH = Path("subs.db")

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    DB_PATH.touch(exist_ok=True)
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            chat_id INTEGER PRIMARY KEY
        );
    """)
    conn.commit()
    conn.close()

def add_sub(chat_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # ВАЖНО: параметр как кортеж
    cur.execute("INSERT OR IGNORE INTO users (chat_id) VALUES (?)", (int(chat_id),))
    conn.commit()
    conn.close()

def del_sub(chat_id: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE chat_id=?", (int(chat_id),))
    conn.commit()
    conn.close()

def all_sub():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT chat_id FROM users")
    rows = [row[0] for row in cur.fetchall()]
    conn.close()
    return rows

def count_subs():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    n = cur.fetchone()[0]
    conn.close()
    return n

# Инициализация БД один раз при импорте
init_db()