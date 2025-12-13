from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import create_user, get_user_by_username, get_user_by_email, verify_user_login

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user_name', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            flash('Заповніть логін і пароль', 'error')
            return render_template('login.html')

        user = verify_user_login(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['is_admin'] = user.get('is_admin', 0)
            flash('Ви успішно увійшли!', 'success')
            return redirect('/')
        else:
            flash('Невірний логін або пароль. Якщо у вас немає акаунту, <a href="/register" class="text-blue-600 underline">зареєструйтесь</a>.', 'error')
            return render_template('login.html')

    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('user_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not email or not password:
            flash('Заповніть усі поля: ім’я, email, пароль', 'error')
            return render_template('register.html')

        if get_user_by_username(username):
            flash('Такий логін вже існує', 'error')
            return render_template('register.html')

        if get_user_by_email(email):
            flash('Такий email вже існує', 'error')
            return render_template('register.html')

        user_id = create_user(username, email, password)
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            session['email'] = email
            session['is_admin'] = 0
            flash('Реєстрація успішна!', 'success')
            return redirect('/')
        else:
            flash('Помилка при створенні користувача', 'error')
            return render_template('register.html')

    return render_template('register.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Ви вийшли з системи', 'info')
    return redirect('/')