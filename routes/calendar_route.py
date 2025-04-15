from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from models import Event, db
from datetime import datetime, timedelta

calendar_bp = Blueprint('calendar', __name__)

# Календарь
@calendar_bp.route('/calendar')
def view_calendar():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    events = Event.query.filter_by(user_id=session['user_id']).order_by(Event.date).all()

    now = datetime.now()
    three_days_later = now + timedelta(days=3)
    upcoming_events = [e for e in events if now <= e.date <= three_days_later]

    return render_template('calendar/view.html', events=events, upcoming_events=upcoming_events)

@calendar_bp.route('/calendar/add', methods=['GET', 'POST'])
def add_event():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date_str = request.form['date']
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Неверный формат даты и времени', 'danger')
            return redirect(url_for('calendar.add_event'))
        
        new_event = Event(
            title=title,
            description=description,
            date=date,
            user_id=session['user_id']
        )
        
        db.session.add(new_event)
        db.session.commit()
        
        flash('Событие успешно добавлено!', 'success')
        return redirect(url_for('calendar.view_calendar'))
    
    return render_template('calendar/add.html')

@calendar_bp.route('/calendar/delete/<int:id>')
def delete_event(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    event = Event.query.get_or_404(id)
    
    db.session.delete(event)
    db.session.commit()
    
    flash('Событие успешно удалено!', 'success')
    return redirect(url_for('calendar.view_calendar'))