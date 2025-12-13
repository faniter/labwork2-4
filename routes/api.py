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
    'responses': {200: {'description': 'List of products'}}
})
def v1_list_products():
    category_id = request.args.get('category_id', type=int)
    search = request.args.get('search', type=str)
    products = get_all_sneakers(category_id=category_id, search=search)
    return jsonify(products), 200


@api_bp.route('/v1/products/<int:product_id>', methods=['GET'])
def v1_get_product(product_id):
    conn = get_db_conn()
    row = conn.execute('SELECT s.*, c.name as category_name FROM sneakers s LEFT JOIN categories c ON s.category_id = c.id WHERE s.id = ?', (product_id,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(dict(row)), 200


@api_bp.route('/v1/products', methods=['POST'])
def v1_create_product():
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
def v1_delete_product(product_id):
    # check exists
    conn = get_db_conn()
    exists = conn.execute('SELECT 1 FROM sneakers WHERE id = ?', (product_id,)).fetchone()
    conn.close()
    if not exists:
        return jsonify({'error': 'Product not found'}), 404
    delete_sneaker(product_id)
    return jsonify({'status': 'deleted'}), 200


@api_bp.route('/v1/categories', methods=['GET'])
def v1_list_categories():
    cats = get_categories()
    return jsonify(cats), 200


@api_bp.route('/v1/feedback', methods=['POST'])
def v1_feedback():
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
def v2_create_product():
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
