# ...existing code...
import os
import runpy
from flask import Flask

from models import init_db, get_db_conn

from routes.shop import shop_bp
from routes.admin import admin_bp
from routes.feedback import feedback_bp
from routes.auth import auth_bp



# Ініціалізація структури БД (створює файл db.sqlite якщо ще нема)
init_db()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY'] = 'your-very-secret-random-key-12345'

app.register_blueprint(shop_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(feedback_bp)
app.register_blueprint(auth_bp)


def ensure_seeded():
    """Якщо в таблиці sneakers немає записів — виконуємо seed.py для наповнення."""
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='sneakers'")
        if cur.fetchone()[0] == 0:
            # таблиці не існують — init_db вже викликаний, але надійність
            init_db()
        cur.execute("SELECT COUNT(*) FROM sneakers")
        count = cur.fetchone()[0]
        conn.close()
    except Exception:
        count = 0

    if count == 0:
        seed_path = os.path.join(os.path.dirname(__file__), 'seed.py')
        if os.path.exists(seed_path):
            # Виконуємо seed.py (виконає додавання категорій/товарів)
            runpy.run_path(seed_path, run_name="__main__")


if __name__ == '__main__':
    ensure_seeded()
    # Запуск аплікації
    app.run(host='0.0.0.0', port=5000, debug=True)
# ...existing code...