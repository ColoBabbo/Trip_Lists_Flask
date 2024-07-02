from flask import render_template, redirect, request, session, url_for, flash
from flask_app import app
from flask_app.models import user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

import time
currently_testing = True

@app.route('/')
def index() -> None:
    if session.get('register_attempt'):
        pre_fill = {
            'first_name': session['register_attempt']['first_name'],
            'last_name': session['register_attempt']['last_name'],
            'email': session['register_attempt']['email'],
            'password': ''
        }
    elif currently_testing:
        timestamp = time.time()
        last5 = str(timestamp)[-5:]
        pre_fill = {
            'first_name': f'Test {last5}',
            'last_name': f'User {last5}',
            'email': f'{last5}@user.com',
            'password': 'secur3Password'
        }
    else:
        pre_fill = {
            'first_name': '',
            'last_name': '',
            'email': '',
            'password': ''
        }
    return render_template('login_registration.html', pre_fill = pre_fill)

@app.route('/register', methods=["GET", "POST"])
def register() -> None:
    if request.method == "POST":
        if user.User.is_legit_registration(request.form):
            pw_hash = bcrypt.generate_password_hash(request.form['password'])
            data = {
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'password': pw_hash
            }
            new_user_id = user.User.insert_one(data)
            session['current_login'] = new_user_id
            session['first_name'] = data['first_name']
            session['logged_in'] = True
            return redirect(url_for('show_all_trips', user_id = new_user_id))
        session['register_attempt'] = request.form
    return redirect('/')

@app.post('/login')
def login() -> None:
    form_data = {
        'email': request.form['login_email'],
        'password': request.form['login_password'],
    }
    this_user = user.User.get_user_if_login_legit(form_data)
    if this_user:
        session['current_login'] = this_user.id
        session['first_name'] = this_user.first_name
        session['logged_in'] = True
        return redirect(url_for('show_all_trips', user_id = this_user.id))
    return redirect('/')

@app.get('/user/<int:user_id>')
def dashboard(user_id:int) -> None:
    if session.get('logged_in') and session.get('current_login') == user_id:
        this_user = user.User.get_one(user_id)
        if session.get('register_attempt'):
            session.pop('register_attempt')
        return render_template('user_profile.html', user = this_user )
    else:
        flash('Please Login', 'login')
    return redirect('/')

@app.get('/user/logout')
def logout() -> None:
    if session.get('register_attempt'):
        session.pop('register_attempt')
    if session.get('current_login'):
        session.pop('current_login')
    if session.get('user_name'):
        session.pop('user_name')
    if session.get('logged_in'):
        session.pop('logged_in')
    if session.get('trip_attempt'):
        session.pop('trip_attempt')
    if session.get('edit_attempt'):
        session.pop('edit_attempt')
    if session.get('item_attempt'):
        session.pop('item_attempt')
    return redirect('/')
