import os
import runpy
from flask import Flask

from models import init_db, get_db_conn

from routes.shop import shop_bp
from routes.admin import admin_bp
from routes.feedback import feedback_bp
from routes.auth import auth_bp
from routes.api import api_bp
from routes.api_demo import api_demo_bp

from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from flasgger import Swagger

# Ініціалізація структури БД (створює файл db.sqlite якщо ще нема)
init_db()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SECRET_KEY']     = '23ae9366-f681-4ac9-a55f-0fb8b0029b4e'
app.config['JWT_SECRET_KEY'] = '8874d6c6-8c0b-43d1-a066-0d674d80d3c1'

# Зареєстровані маршрути
app.register_blueprint(shop_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(feedback_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(api_demo_bp)



# Swagger (API documentation)
app.config['SWAGGER'] = {
    'title': 'Labwork API',
    'uiversion': 3
}
Swagger(app)




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


# JSON error handlers
@app.errorhandler(400)
def bad_request(e):
    return {'error': 'Bad Request'}, 400


@app.errorhandler(404)
def not_found(e):
    return {'error': 'Not Found'}, 404


@app.errorhandler(500)
def server_error(e):
    return {'error': 'Internal Server Error'}, 500


if __name__ == '__main__':
    ensure_seeded()
    # Запуск аплікації
    app.run(host='0.0.0.0', port=5000, debug=True)
