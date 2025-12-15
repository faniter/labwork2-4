# ...existing code...
import sqlite3
import os
from typing import List, Optional, Dict, Any

DB_NAME = 'db.sqlite'

def get_db_path() -> str:
    """Повертає шлях до файлу БД: спочатку читає ENV `DATABASE_PATH`, інакше повертає дефолтний шлях поруч з модулем."""
    env_path = os.environ.get('DATABASE_PATH')
    if env_path:
        return env_path
    return os.path.join(os.path.dirname(__file__), DB_NAME)


def get_db_conn():
    db_path = get_db_path()
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sneakers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL,
        image_url TEXT,
        category_id INTEGER,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT,
        email TEXT,
        message TEXT,
        created_at TEXT DEFAULT (datetime('now'))
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    )
    ''')

    conn.commit()
    conn.close()

def add_sneaker(name: str, description: str, price: float, image_url: str, category_id: Optional[int] = None) -> int:
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sneakers (name, description, price, image_url, category_id)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, description, price, image_url, category_id))
    conn.commit()
    sneaker_id = cursor.lastrowid
    conn.close()
    return sneaker_id

def get_all_sneakers(category_id: Optional[int] = None, search: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db_conn()
    cursor = conn.cursor()
    sql = "SELECT s.*, c.name as category_name FROM sneakers s LEFT JOIN categories c ON s.category_id = c.id"
    params = []
    where = []
    if category_id:
        where.append("s.category_id = ?")
        params.append(category_id)
    if search:
        where.append("(s.name LIKE ? OR s.description LIKE ?)")
        q = f"%{search}%"
        params.extend([q, q])
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY s.id DESC"
    rows = cursor.execute(sql, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_sneaker(sneaker_id: int) -> None:
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sneakers WHERE id = ?", (sneaker_id,))
    conn.commit()
    conn.close()

def get_categories() -> List[Dict[str, Any]]:
    conn = get_db_conn()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM categories ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def create_user(username: str, email: str, password: str) -> Optional[int]:
    conn = get_db_conn()
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        ''', (username, email, password))
        conn.commit()
        user_id = cur.lastrowid
        return user_id
    except Exception:
        return None
    finally:
        conn.close()

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    conn = get_db_conn()
    row = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    conn = get_db_conn()
    row = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return dict(row) if row else None

def verify_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    conn = get_db_conn()
    row = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
    conn.close()
    return dict(row) if row else None

def verify_user_login(login: str, password: str) -> Optional[Dict[str, Any]]:
    """Перевірка користувача за username + пароль"""
    conn = get_db_conn()
    row = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (login, password)).fetchone()
    conn.close()
    return dict(row) if row else None
# ...existing code...