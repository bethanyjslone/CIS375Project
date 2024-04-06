# PillLibraryApp/routes.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash
from datetime import datetime
from .models import db, User, Medication
from .forms import LoginForm, RegistrationForm

# Create a Blueprint for your main routes
main = Blueprint('main', __name__)

@main.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    meds = Medication.query.filter_by(user_id=session['user_id']).all()
    return render_template('calendar.html', meds=meds)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            session['logged_in'] = True
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password')

    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    return redirect(url_for('main.login'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main.tracker'))

    return render_template('register.html', form=form)

@main.route('/medication/add', methods=['POST'])
def add_medication():
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    new_med = Medication(
        name=request.form['name'],
        dosage=request.form['dosage'],
        frequency=request.form['frequency'],
        start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
        end_date=(datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
                  if request.form['end_date'] else None),
        notes=request.form['notes'],
        user_id=session['user_id']
    )
    db.session.add(new_med)
    db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/medication/edit/<int:medication_id>', methods=['POST'])
def edit_medication(medication_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    med = Medication.query.get(medication_id)
    if med and med.user_id == session['user_id']:
        med.name=request.form['name'],
        med.dosage=request.form['dosage'],
        med.frequency=request.form['frequency'],
        med.start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
        med.end_date=(datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
                      if request.form['end_date'] else None),
        med.notes=request.form['notes']
        db.session.commit()

    return redirect(url_for('main.index'))

@main.route('/medication/delete/<int:medication_id>', methods=['GET'])
def delete_medication(medication_id):
    if 'user_id' not in session:
        return redirect(url_for('main.login'))

    Medication.query.filter_by(id=medication_id, user_id=session['user_id']).delete()
    db.session.commit()

    return redirect(url_for('main.index'))