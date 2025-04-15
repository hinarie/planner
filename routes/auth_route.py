from flask import Blueprint, request, session, flash, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db

auth_bp = Blueprint('auth', __name__)

# Аутентификация
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        
        if user and check_password_hash(user.password, request.form['password']):
            session.update({
                'user_id': user.id,
                'username': user.username,
                'name': user.name
            })
            flash('Вы успешно вошли в систему!', 'success')
            return redirect(url_for('home'))
        
        flash('Неверное имя пользователя или пароль', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('Пользователь с таким именем уже существует', 'danger')
            return redirect(url_for('auth.register'))
        
        user = User(
            username=request.form['username'],
            password=generate_password_hash(request.form['password']),
            name=request.form['name']
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация прошла успешно! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('auth.login'))