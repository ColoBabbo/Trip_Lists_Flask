from flask import render_template, redirect, request, session, url_for, flash, jsonify
from flask_app import app
from flask_app.models import trip, item

@app.post('/trip/<int:trip_id>/list/<int:list_id>/item/<int:item_id>/edit/json')
def edit_item(trip_id:int, list_id:int, item_id:int) -> None:
    updated_item = item.Item.update_one_json(request.form)
    return jsonify({'return_item':request.form})

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
                    'is_packed': session['item_attempt']['is_packed'],
                }
            else:
                pre_fill = {
                    'name': '',
                    'unit': '',
                    'quantity': '',
                    'is_packed': False,
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
                    return redirect(url_for('show_one_list', trip_id = request.form['trip_id'], list_id = request.form['list_id']) )
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

@app.route('/trip/<int:trip_id>/list/<int:list_id>/item/<int:item_id>', methods=["GET", "POST"])
def show_one_item(trip_id:int, list_id:int, item_id:int):
    if session.get('logged_in'):
        if request.method == "GET":
            this_item = item.Item.get_one(item_id)
            if this_item == False:
                flash('No such record!', 'unauthorized')
                return redirect(url_for('show_all_trips'))
            elif this_item.user_id != session.get('current_login'):
                flash("That's not yours!", 'unauthorized')
                return redirect(url_for('show_all_trips'))
            if session.get('item_attempt'):
                pre_fill = {
                    'name': session['item_attempt']['name'],
                    'unit': session['item_attempt']['unit'],
                    'quantity': session['item_attempt']['quantity'],
                    # 'is_packed': session['item_attempt']['is_packed'],
                }
            else:
                pre_fill = {
                    'name': this_item.name,
                    'unit': this_item.unit,
                    'quantity': this_item.quantity,
                    # 'is_packed': this_item.is_packed,
                }
            return render_template('show_one_item.html', trip_id = trip_id, pre_fill = pre_fill, list_id = list_id, this_item = this_item)
        elif request.method == "POST":
            if item.Item.is_legit_item(request.form):
                form_data = {
                    'name': request.form['name'],
                    'unit': request.form['unit'],
                    'quantity': request.form['quantity'],
                    'is_packed': (1 if request.form.get(f'is_packed_for_item_{item_id}') else 0),
                    'item_id': request.form['item_id'],
                }
                updated_item = item.Item.update_one(form_data)
                if session.get('item_attempt'):
                    session.pop('item_attempt')
                return redirect(url_for('show_one_item', trip_id = trip_id, list_id = list_id, item_id = item_id))
            session['item_attempt'] = request.form
        return redirect(url_for('show_one_item', trip_id = trip_id, list_id = list_id, item_id = item_id))
    else:
        flash('Please Login', 'login')
    return redirect('/')

@app.route('/trip/<int:trip_id>/list/<int:list_id>/item/<int:item_id>/delete')
def delete_item(trip_id:int, list_id:int, item_id:int) -> None:
    if session.get('logged_in'):
        this_trip:object = trip.Trip.get_one(trip_id)
        if not this_trip:
            flash('No such record!', 'unauthorized')
            return redirect(url_for('show_all_trips'))
        if not this_trip.lists.get(list_id):
            flash('No such List!', 'unauthorized')
            return redirect(url_for('show_all_trips'))
        elif this_trip.user_id != session.get('current_login'):
            flash("That's not yours!", 'unauthorized')
            return redirect(url_for('show_all_trips'))
        item.Item.delete_one(item_id)
        return redirect(url_for('show_one_list', trip_id = trip_id, list_id = list_id))
    else:
        flash('Please Login', 'login')
    return redirect('/')
