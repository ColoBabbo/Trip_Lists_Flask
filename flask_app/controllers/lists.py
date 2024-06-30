from flask import render_template, redirect, request, session, url_for, flash
from flask_app import app
from flask_app.models import trip, list

@app.route('/add_list', methods=["GET", "POST"])
def add_list() -> None:
    if session.get('logged_in'):
        if request.method == "GET":
            if session.get('list_attempt'):
                pre_fill = {
                    'new_list': session['list_attempt']['new_list'],
                }
            else:
                pre_fill = {
                    'new_list': '',
                }
            return render_template('show_one_trip.html', pre_fill = pre_fill)
        elif request.method == "POST":
            if list.List.is_legit_list(request.form):
                new_list = list.List.insert_one(request.form)
                if session.get('list_attempt'):
                    session.pop('list_attempt')
                return redirect(url_for('show_one_trip', trip_id = request.form['trip_id']) )
            session['list_attempt'] = request.form
        return redirect(url_for('show_one_trip', trip_id = request.form['trip_id']) )
    else:
        flash('Please Login', 'login')
    return redirect('/dashboard')

@app.get('/trip/<int:trip_id>/list/<int:list_id>')
def show_one_list(trip_id:int, list_id:int):
    if session.get('logged_in'):
        this_trip = trip.Trip.get_one(trip_id)
        if this_trip == False:
            flash('No such record!', 'unauthorized')
            return redirect(url_for('show_all_trips'))
        if session.get('list_attempt'):
            pre_fill = {
                'list_name': session['list_attempt']['list_name'],
            }
        else:
            pre_fill = {
                'list_name': '',
            }
        return render_template('show_one_list.html', this_trip = this_trip, pre_fill = pre_fill, list_id = list_id)
    else:
        flash('Please Login', 'login')
    return redirect('/')
