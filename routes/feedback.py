from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import get_db_conn

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['GET', 'POST'])
def handle_feedback():
    if request.method == 'POST':
        try:
            user_name = request.form.get('user_name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            if not user_name or not email or not message:
                flash('Будь ласка, заповніть всі поля!', 'error')
                return redirect(url_for('feedback.handle_feedback'))
            
            conn = get_db_conn()
            conn.execute(
                'INSERT INTO feedback (user_name, email, message) VALUES (?, ?, ?)',
                (user_name, email, message)
            )
            conn.commit()
            conn.close()
            
            flash('Дякуємо за ваш відгук! Ми обов\'язково його розглянемо.', 'success')
            return redirect(url_for('feedback.handle_feedback'))
        except Exception as e:
            flash(f'Помилка при збереженні відгуку: {str(e)}', 'error')
            return redirect(url_for('feedback.handle_feedback'))
    
    return render_template('feedback.html')

@feedback_bp.route('/api/feedback', methods=['GET', 'POST'])
def handle_api_feedback():
    
    if request.method == 'POST':
        
        user_name = request.form['user_name']
        email = request.form['email']
        message = request.form['message']
        
        
        conn = get_db_conn()
        conn.execute(
            'INSERT INTO feedback (user_name, email, message) VALUES (?, ?, ?)',
            (user_name, email, message)
        )
        conn.commit()
        conn.close()
        
        
        return redirect(url_for('shop.home'))

    
    conn = get_db_conn()
    feedbacks = conn.execute('SELECT * FROM feedback ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify(feedbacks)
