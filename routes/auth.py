# routes/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# Создаем Blueprint для авторизации
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Временная заглушка
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        
        # Простая проверка для теста
        if email == 'test@test.com' and password == '123':
            session['user_id'] = 1
            session['username'] = 'Тестовий користувач'
            session['email'] = email
            session['is_admin'] = 0
            flash('Ви успішно увійшли!', 'success')
            return redirect('/')
        else:
            flash('Невірний email або пароль', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Временная заглушка
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        
        # Простая регистрация для теста
        session['user_id'] = 2
        session['username'] = username
        session['email'] = email
        session['is_admin'] = 0
        
        flash('Реєстрація успішна!', 'success')
        return redirect('/')
    
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Ви вийшли з системи', 'info')
    return redirect('/')