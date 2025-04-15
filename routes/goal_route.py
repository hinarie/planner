from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from models import Goal, db
from datetime import datetime

goal_bp = Blueprint('goal', __name__)

# Цели
@goal_bp.route('/goals')
def list_goals():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    goals = Goal.query.filter(Goal.user_id == session['user_id']).order_by(Goal.deadline).all()
    return render_template('goals/list.html', goals=goals)

@goal_bp.route('/goals/add', methods=['GET', 'POST'])
def add_goal():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        deadline_str = request.form['deadline']
        
        try:
            deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        except ValueError:
            deadline = None
        
        new_goal = Goal(
            title=title,
            description=description,
            deadline=deadline,
            user_id=session['user_id']
        )
        
        db.session.add(new_goal)
        db.session.commit()
        
        flash('Цель успешно добавлена!', 'success')
        return redirect(url_for('goal.list_goals'))
    
    return render_template('goals/add.html')

@goal_bp.route('/goals/toggle/<int:id>', methods=['POST'])
def toggle_goal(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    goal = Goal.query.get_or_404(id)
    
    goal.is_completed = not goal.is_completed
    db.session.commit()
    
    flash('Статус цели обновлен!', 'success')
    return redirect(url_for('goal.list_goals'))

@goal_bp.route('/goals/delete/<int:id>')
def delete_goal(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    goal = Goal.query.get_or_404(id)
    
    db.session.delete(goal)
    db.session.commit()
    
    flash('Цель успешно удалена!', 'success')
    return redirect(url_for('goal.list_goals'))