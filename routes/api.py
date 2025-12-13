from flask import Blueprint, request, jsonify, abort
from models import get_all_sneakers, add_sneaker, delete_sneaker, get_db_conn, get_categories
try:
    from flasgger import swag_from
except Exception:
    # If flasgger is not installed, provide a no-op decorator so the app still runs.
    def swag_from(_=None):
        def decorator(f):
            return f
        return decorator

api_bp = Blueprint('api', __name__)


# === v1 endpoints (more permissive) ===

@api_bp.route('/v1/products', methods=['GET'])
@swag_from({
    'summary': 'Отримати список всіх товарів',
    'description': 'Повертає список sneakers з можливістю фільтрації за категорією та пошуком',
    'parameters': [
        {
            'name': 'category_id',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'description': 'ID категорії для фільтрації'
        },
        {
            'name': 'search',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Пошуковий запит (в назві або описі)'
        }
    ],
    'responses': {
        200: {
            'description': 'Список товарів',
            'examples': {
                'application/json': [
                    {
                        'id': 1,
                        'name': 'Nike Air Max',
                        'description': 'Classic sneakers',
                        'price': 120.0,
                        'image_url': '/static/uploads/nike.jpg',
                        'category_id': 1,
                        'category_name': 'Running'
                    }
                ]
            }
        }
    }
})
def v1_list_products():
    """Отримати список товарів"""
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', type=str)
    products = get_all_sneakers(category_id=category_id, search=search)
    return jsonify(products), 200


@api_bp.route('/v1/products/<int:product_id>', methods=['GET'])
@swag_from({
    'summary': 'Отримати товар за ID',
    'parameters': [
        {
            'name': 'product_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID товару'
        }
    ],
    'responses': {
        200: {
            'description': 'Деталі товару',
            'examples': {
                'application/json': {
                    'id': 1,
                    'name': 'Nike Air Max',
                    'description': 'Classic sneakers',
                    'price': 120.0,
                    'image_url': '/static/uploads/nike.jpg',
                    'category_id': 1,
                    'category_name': 'Running'
                }
            }
        },
        404: {
            'description': 'Товар не знайдено',
            'examples': {'application/json': {'error': 'Product not found'}}
        }
    }
})
def v1_get_product(product_id):
    """Отримати товар за ID"""
    conn = get_db_conn()
    row = conn.execute('SELECT s.*, c.name as category_name FROM sneakers s LEFT JOIN categories c ON s.category_id = c.id WHERE s.id = ?', (product_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(dict(row)), 200


@api_bp.route('/v1/products', methods=['POST'])
@swag_from({
    'summary': 'Створити новий товар',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name', 'price'],
                'properties': {
                    'name': {'type': 'string', 'example': 'Adidas Ultraboost'},
                    'price': {'type': 'number', 'example': 150.0},
                    'description': {'type': 'string', 'example': 'Comfortable running shoes'},
                    'image_url': {'type': 'string', 'example': '/static/uploads/adidas.jpg'},
                    'category_id': {'type': 'integer', 'example': 1}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Товар створено',
            'examples': {'application/json': {'id': 5}}
        },
        400: {
            'description': 'Невалідні дані',
            'examples': {'application/json': {'error': 'Missing "name" or "price"'}}
        }
    }
})
def v1_create_product():
    """Створити новий товар"""
    data = request.get_json() or {}
    name = data.get('name')
    price = data.get('price')
    if not name or price is None:
        return jsonify({'error': 'Missing "name" or "price"'}), 400
    try:
        price = float(price)
    except Exception:
        return jsonify({'error': 'Invalid price format'}), 400
    description = data.get('description', '')
    image_url = data.get('image_url', '')
    category_id = data.get('category_id')
    sneaker_id = add_sneaker(name, description, price, image_url, category_id)
    return jsonify({'id': sneaker_id}), 201


@api_bp.route('/v1/products/<int:product_id>', methods=['DELETE'])
@swag_from({
    'summary': 'Видалити товар',
    'parameters': [
        {
            'name': 'product_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID товару для видалення'
        }
    ],
    'responses': {
        200: {
            'description': 'Товар видалено',
            'examples': {'application/json': {'status': 'deleted'}}
        },
        404: {
            'description': 'Товар не знайдено',
            'examples': {'application/json': {'error': 'Product not found'}}
        }
    }
})
def v1_delete_product(product_id):
    """Видалити товар за ID"""
    # check exists
    conn = get_db_conn()
    exists = conn.execute('SELECT 1 FROM sneakers WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if not exists:
        return jsonify({'error': 'Product not found'}), 404
    delete_sneaker(product_id)
    return jsonify({'status': 'deleted'}), 200


@api_bp.route('/v1/categories', methods=['GET'])
@swag_from({
    'summary': 'Отримати список категорій',
    'responses': {
        200: {
            'description': 'Список категорій',
            'examples': {
                'application/json': [
                    {'id': 1, 'name': 'Running'},
                    {'id': 2, 'name': 'Basketball'}
                ]
            }
        }
    }
})
def v1_list_categories():
    """Отримати всі категорії"""
    cats = get_categories()
    return jsonify(cats), 200


@api_bp.route('/v1/feedback', methods=['POST'])
@swag_from({
    'summary': 'Надіслати відгук',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['message'],
                'properties': {
                    'user_name': {'type': 'string', 'example': 'Іван Іванов'},
                    'email': {'type': 'string', 'example': 'ivan@example.com'},
                    'message': {'type': 'string', 'example': 'Дуже подобається ваш магазин!'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Відгук створено',
            'examples': {'application/json': {'status': 'ok'}}
        },
        400: {
            'description': 'Поле message обов\'язкове',
            'examples': {'application/json': {'error': 'Message is required'}}
        }
    }
})
def v1_feedback():
    """Надіслати відгук"""
    data = request.get_json() or {}
    user_name = data.get('user_name')
    email = data.get('email')
    message = data.get('message')
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    conn = get_db_conn()
    conn.execute('INSERT INTO feedback (user_name, email, message) VALUES (?, ?, ?)', (user_name, email, message))
    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'}), 201


# === v2 endpoints (stricter validation, example of versioning) ===

@api_bp.route('/v2/products', methods=['POST'])
@swag_from({
    'summary': 'Створити товар (v2 - строга валідація)',
    'description': 'Версія 2 API з посиленою валідацією полів та поверненням повного об\'єкту товару',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['name', 'price'],
                'properties': {
                    'name': {'type': 'string', 'example': 'Puma RS-X'},
                    'price': {'type': 'number', 'example': 110.0},
                    'description': {'type': 'string', 'example': 'Modern retro style'},
                    'image_url': {'type': 'string', 'example': '/static/uploads/puma.jpg'},
                    'category_id': {'type': 'integer', 'example': 2}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Товар створено, повертає повний об\'єкт',
            'examples': {
                'application/json': {
                    'id': 6,
                    'name': 'Puma RS-X',
                    'description': 'Modern retro style',
                    'price': 110.0,
                    'image_url': '/static/uploads/puma.jpg',
                    'category_id': 2,
                    'category_name': 'Casual'
                }
            }
        },
        400: {
            'description': 'Помилка валідації',
            'examples': {'application/json': {'error': 'Field "name" must be a non-empty string'}}
        }
    }
})
def v2_create_product():
    """Створити товар з строгою валідацією (API v2)"""
    data = request.get_json() or {}
    # stricter validation
    if not isinstance(data.get('name'), str) or not data.get('name'):
        return jsonify({'error': 'Field "name" must be a non-empty string'}), 400
    try:
        price = float(data.get('price'))
    except Exception:
        return jsonify({'error': 'Field "price" must be a number'}), 400
    description = data.get('description', '')
    image_url = data.get('image_url', '')
    category_id = data.get('category_id')
    sneaker_id = add_sneaker(data['name'], description, price, image_url, category_id)
    # return created resource
    conn = get_db_conn()
    row = conn.execute('SELECT s.*, c.name as category_name FROM sneakers s LEFT JOIN categories c ON s.category_id = c.id WHERE s.id = ?', (sneaker_id,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201
