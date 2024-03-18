from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask import redirect, url_for
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note.strip()) > 0:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
            return redirect(url_for('views.home'))
        else:
            flash('Note is too short!', category='error')

    return render_template("home.html", user=current_user)

@views.route('/edit-note/<int:note_id>', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get(note_id)

    if current_user.id != note.user_id:
        return render_template("error.html", message="Unauthorized to edit note")

    if request.method == 'POST':
        new_data = request.form.get('note')

        if len(new_data.strip()) > 0:
            note.data = new_data
            db.session.commit()
            flash('Note updated!', category='success')
            return redirect(url_for('views.home'))  # Redirect to home page after editing
        else:
            flash('Note is too short!', category='error')

    return render_template("home.html",user=current_user, note=note)  # Render edit note template


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
