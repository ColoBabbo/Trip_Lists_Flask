from flask import render_template, redirect, request, session, url_for, flash, jsonify
from flask_app import app
from flask_app.models import trip

@app.route('/trip/<int:trip_id>/json')
def show_one_trip_json(trip_id:int):
    if session.get('logged_in'):
        this_trip = trip.Trip.get_one_json(trip_id)
        if session.get('item_attempt'):
            session.pop('item_attempt')
        return jsonify({'this_trip_json' : this_trip})
    else:
        flash('Please Login', 'login')
    return redirect('/')

@app.get('/trip/<int:trip_id>')
def show_one_trip(trip_id:int):
    if session.get('logged_in'):
        this_trip = trip.Trip.get_one(trip_id)
        if this_trip == False:
            flash('No such record!', 'unauthorized')
            return redirect(url_for('show_all_trips'))
        elif this_trip.user.id != session.get('current_login'):
            flash("That's not yours!", 'unauthorized')
            return redirect(url_for('show_all_trips'))
        if session.get('list_attempt'):
            pre_fill = {
                'list_name': session['list_attempt']['list_name'],
            }
        else:
            pre_fill = {
                'list_name': '',
            }
        return render_template('show_one_trip.html', this_trip = this_trip, pre_fill = pre_fill)
    else:
        flash('Please Login', 'login')
    return redirect('/')

@app.get('/dashboard')
def show_all_trips():
    if session.get('logged_in'):
        all_trips = trip.Trip.get_all()
        if session.get('item_attempt'):
            session.pop('item_attempt')
        return render_template('show_all_trips.html', all_trips = all_trips)
    else:
        flash('Please Login', 'login')
    return redirect('/')

@app.route('/add_trip', methods=["GET", "POST"])
def add_trip() -> None:
    if session.get('logged_in'):
        if session.get('item_attempt'):
            session.pop('item_attempt')
        if request.method == "GET":
            if session.get('trip_attempt'):
                pre_fill = {
                    'name': session['trip_attempt']['name'],
                    'location': session['trip_attempt']['location'],
                    'days': session['trip_attempt']['days'],
                    'date': session['trip_attempt']['date'],
                }
            else:
                pre_fill = {
                    'name': '',
                    'location': '',
                    'days': '',
                    'date': '',
                }
            return render_template('new_trip.html', pre_fill = pre_fill)
        elif request.method == "POST":
            if trip.Trip.is_legit_trip(request.form):
                new_trip = trip.Trip.insert_one(request.form)
                if session.get('trip_attempt'):
                    session.pop('trip_attempt')
                return redirect(url_for('show_all_trips'))
            session['trip_attempt'] = request.form
        return redirect('/add_trip')
    else:
        flash('Please Login', 'login')
    return redirect('/dashboard')

@app.get('/trip/<int:trip_id>/delete')
def delete_trip(trip_id:int) -> None:
    if session.get('logged_in'):
        if session.get('item_attempt'):
            session.pop('item_attempt')
        this_trip = trip.Trip.get_one(trip_id)
        if not this_trip:
            flash('No such record!', 'unauthorized')
            return redirect(url_for('show_all_trips'))
        elif this_trip.user_id != session.get('current_login'):
            flash("That's not yours!", 'unauthorized')
            return redirect(url_for('show_all_trips'))
        trip.Trip.delete_one(trip_id)
        return redirect(url_for('show_all_trips'))
    else:
        flash('Please Login', 'login')
    return redirect('/')

@app.route('/trip/<int:trip_id>/edit', methods=["GET", "POST"])
def edit_trip(trip_id:int) -> None:
    this_trip = trip.Trip.get_one(trip_id)
    if not this_trip:
        flash('No such record!', 'unauthorized')
        return redirect(url_for('show_all_trips'))
    elif this_trip.user_id != session.get('current_login'):
        flash("That's not yours!", 'unauthorized')
        return redirect(url_for('show_all_trips'))
    if session.get('logged_in'):
        if request.method == "GET":
            if session.get('edit_attempt'):
                pre_fill = {
                    'name': session['edit_attempt']['name'],
                    'date': session['edit_attempt']['date'],
                    'location': session['edit_attempt']['location'],
                    'days': session['edit_attempt']['days'],
                }
            else:
                pre_fill = {
                    'name': this_trip.name,
                    'date': this_trip.date,
                    'location': this_trip.location,
                    'days': this_trip.days,
                }
            return render_template('edit_trip.html', pre_fill = pre_fill, trip_id = trip_id)
        elif request.method == "POST":
            if trip.Trip.is_legit_trip(request.form):
                updated_trip = trip.Trip.update_one(request.form)
                if session.get('edit_attempt'):
                    session.pop('edit_attempt')
                return redirect(url_for('show_one_trip', trip_id = trip_id))
            session['edit_attempt'] = request.form
        return redirect(url_for('edit_trip', trip_id = trip_id))
    else:
        flash('Please Login', 'login')
    return redirect('/')

@app.get('/trip/<int:trip_id>/edit/link')
def edit_trip_from_link(trip_id:int) -> None:
    if session.get('logged_in'):
        if session.get('edit_attempt'):
            session.pop('edit_attempt')
    else:
        flash('Please Login', 'login')
    return redirect(url_for('edit_trip', trip_id = trip_id))