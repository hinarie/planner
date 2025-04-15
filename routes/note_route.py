from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from models import Note, db

note_bp = Blueprint('note', __name__)

# Заметки
@note_bp.route('/notes/personal')
def personal_notes():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    notes = Note.query.filter_by(user_id=session['user_id'], is_private=True).order_by(Note.date_created.desc()).all()
    return render_template('notes/personal.html', notes=notes)

@note_bp.route('/notes/add', methods=['GET', 'POST'])
def add_note():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if not title or not content:
            flash('Пожалуйста, заполните все обязательные поля', 'danger')
            return redirect(url_for('note.add_note'))
        
        note = Note(
            title=title,
            content=content,
            is_private=True,
            user_id=session['user_id']
        )
        db.session.add(note)
        db.session.commit()
        flash('Заметка успешно добавлена!', 'success')
        return redirect(url_for('note.personal_notes'))
    
    return render_template('notes/add.html')

@note_bp.route('/notes/<int:id>')
def view_note(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    note = Note.query.get_or_404(id)
    
    return render_template('notes/view.html', note=note)

@note_bp.route('/notes/edit/<int:id>', methods=['GET', 'POST'])
def edit_note(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    note = Note.query.get_or_404(id)
    
    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('content')
        note.is_private = True
        db.session.commit()
        flash('Заметка успешно обновлена!', 'success')
        return redirect(url_for('note.view_note', id=note.id))
    
    return render_template('notes/edit.html', note=note)

@note_bp.route('/notes/delete/<int:id>')
def delete_note(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    note = Note.query.get_or_404(id)
    
    db.session.delete(note)
    db.session.commit()
    flash('Заметка успешно удалена!', 'success')
    return redirect(url_for('note.personal_notes'))