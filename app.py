from flask import Flask, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
from config import Config
from models import db, User, Event, Goal, Note
from routes.auth_route import auth_bp
from routes.note_route import note_bp
from routes.goal_route import goal_bp
from routes.calendar_route import calendar_bp

# Инициализация приложения
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Контекстный процессор для добавления datetime во все шаблоны
@app.context_processor
def inject_datetime():
    return {'datetime': datetime}

with app.app_context():
    db.create_all()
    print("База данных успешно инициализирована.")

# Главная страница
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    
    data = {
        'user': user,
        'personal_notes': Note.query.filter_by(user_id=session['user_id'], is_private=True).order_by(Note.date_created.desc()).all(),
        'goals': Goal.query.filter(Goal.user_id == session['user_id']).order_by(Goal.deadline).all(),
        'upcoming_events': Event.query.filter(Event.user_id == session['user_id'], Event.date >= datetime.now()).order_by(Event.date).limit(5).all()
    }
    
    return render_template('home.html', **data)

app.register_blueprint(auth_bp)
app.register_blueprint(note_bp)
app.register_blueprint(goal_bp)
app.register_blueprint(calendar_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))