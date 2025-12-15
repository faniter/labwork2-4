from flask import Blueprint, render_template

api_demo_bp = Blueprint('api_demo', __name__)

@api_demo_bp.route('/api-demo', methods=['GET'])
def api_demo_page():
    """Сторінка демонстрації роботи з API"""
    return render_template('api_demo.html')
