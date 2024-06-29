from flask import render_template, redirect, request, session, url_for, flash
from flask_app import app
from flask_app.models import trip, list, item

@app.route('/add_item', methods=["GET", "POST"])
def add_item() -> None:
    if session.get('logged_in'):
        if request.method == "GET":
            if not session.get('add_new_item'):
                flash('Please select a List before adding Items!', 'unauthorized_minor')
                return redirect(url_for('show_all_trips'))
            if session.get('item_attempt'):
                pre_fill = {
                    'name': session['item_attempt']['name'],
                    'unit': session['item_attempt']['unit'],
                    'quantity': session['item_attempt']['quantity'],
                }
            else:
                pre_fill = {
                    'name': '',
                    'unit': '',
                    'quantity': '',
                }
            return render_template('new_item.html', pre_fill = pre_fill)
        elif request.method == "POST":
            if not request.form.get('from_list_button'):
                if item.Item.is_legit_item(request.form):
                    new_item = item.Item.insert_one(request.form)
                    if session.get('item_attempt'):
                        session.pop('item_attempt')
                    if session.get('add_new_item'):
                        session.pop('add_new_item')
                    return redirect(url_for('show_one_trip', trip_id = request.form['trip_id'], list_id = request.form['list_id']) )
                return redirect(url_for('add_item') )
            else:
                session['add_new_item'] = request.form
                if session.get('item_attempt'):
                    session.pop('item_attempt')
                return redirect(url_for('add_item') )
        return redirect(url_for('show_one_trip', trip_id = request.form['trip_id']) )
    else:
        flash('Please Login', 'login')
    return redirect('/dashboard')