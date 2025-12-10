# ...existing code...
import sqlite3
import os
from typing import List, Optional, Dict, Any

DB_NAME = 'db.sqlite'

def get_db_conn():
    db_path = os.path.join(os.path.dirname(__file__), DB_NAME)
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
# ...existing code...