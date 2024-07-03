from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import list, user, item

class Trip:
    db = 'trip_lists_flask_db'

    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.location = data['location']
        self.date = data['date']
        self.days = data['days']
        self.user = {}
        self.lists = {}

    def __repr__(self) -> str:
        return f'Trip {self.name}, self.lists = {self.lists}'

    @classmethod
    def get_one_json(cls, trip_id:int) -> object:
        query = """
                SELECT trips.id, trips.name, date, days, location, 
                    user_id, users.id, first_name, last_name, email, 
                    lists.id, lists.name, trip_id, 
                    items.id, items.name, unit, quantity, list_id, is_packed 
                FROM trips
                LEFT JOIN users ON trips.user_id = users.id
                LEFT JOIN lists ON lists.trip_id = trips.id
                LEFT JOIN items ON items.list_id = lists.id
                WHERE trips.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'id': trip_id})
        return results

    @classmethod
    def get_all(cls) -> list:
        query = """
                SELECT * FROM trips
                LEFT JOIN users ON trips.user_id = users.id
                WHERE users.id = %(user_id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'user_id' : session.get('current_login')})
        all_trips = []
        for trip in results:
            this_trip = cls(trip)
            user_data = {
                'id': trip['users.id'],
                'first_name': trip['first_name'],
                'last_name': trip['last_name'],
                'email': trip['email'],
            }
            this_trip_user = user.User(user_data)
            this_trip.user = this_trip_user
            all_trips.append(this_trip)
        return all_trips

    @classmethod
    def get_one(cls, trip_id:int) -> object:
        query = """
                SELECT * FROM trips
                LEFT JOIN users ON trips.user_id = users.id
                LEFT JOIN lists ON lists.trip_id = trips.id
                LEFT JOIN items ON items.list_id = lists.id
                WHERE trips.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'id': trip_id})
        if results:
            this_result = results[0]
            this_trip = cls(this_result)
            user_data = {
                'id': this_result['users.id'],
                'first_name': this_result['first_name'],
                'last_name': this_result['last_name'],
                'email': this_result['email'],
            }
            this_trip_user = user.User(user_data)
            this_trip.user = this_trip_user
            for each_list in results:
                if each_list['list_id'] not in this_trip.lists:
                    list_data = {
                        'id': each_list['lists.id'],
                        'name': each_list['lists.name'],
                        'trip_id': each_list['trip_id'],
                    }
                    this_trip_list = list.List(list_data)
                    this_trip.lists[this_trip_list.id] = this_trip_list
                    
                    item_data = {
                        'id': each_list['items.id'],
                        'name': each_list['items.name'],
                        'unit': each_list['unit'],
                        'quantity': each_list['quantity'],
                        'is_packed': each_list['is_packed'],
                        'list_id': each_list['list_id'],
                    }
                    this_trip_item = item.Item(item_data)
                    this_trip.lists[this_trip_list.id].items.append(this_trip_item)
                else:
                    item_data = {
                        'id': each_list['items.id'],
                        'name': each_list['items.name'],
                        'unit': each_list['unit'],
                        'quantity': each_list['quantity'],
                        'is_packed': each_list['is_packed'],
                        'list_id': each_list['list_id'],
                    }
                    existing_trip_item = item.Item(item_data)
                    this_trip.lists[each_list['list_id']].items.append(existing_trip_item)
            return this_trip
        else:
            return False

    @classmethod
    def check_one_by_name(cls, name:str) -> bool:
        query = """
                SELECT * FROM trips
                WHERE name = %(name)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'name': name})
        if results:
            return True
        else:
            return False

    @classmethod
    def update_one(cls, form_dict:dict) -> None:
        query = """
                UPDATE trips
                SET name = %(name)s, days =  %(days)s, location = %(location)s, date = %(date)s
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, form_dict)

    @classmethod
    def insert_one(cls, form_dict:dict) -> int:
        query = """
                INSERT INTO trips (name, days, location, date, user_id)
                VALUES (%(name)s, %(days)s, %(location)s, %(date)s, %(user_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, form_dict)

    @classmethod
    def delete_one(cls, trip_id:int) -> None:
        query = """
                DELETE FROM trips
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {"id": trip_id})

    @classmethod
    def is_legit_trip(cls, form_dict:dict) -> bool:
        valid_input = True
        if not len(form_dict.get('name')) > 0 :
            flash('Your trip needs a name!', 'name')
            valid_input = False
        elif not len(form_dict.get('name')) >= 3:
            flash('name must be at least 3 characters.', 'name')
            valid_input = False
        elif cls.check_one_by_name(form_dict.get('name')) and form_dict.get('new_trip'):
            flash(f'This trip has already been added.', 'name')
            valid_input = False
        if not len(form_dict.get('location')) > 0 :
            flash('Your trip needs a Location!', 'location')
            valid_input = False
        elif not len(form_dict.get('location')) >= 3:
            flash('Location must be at least 3 characters.', 'location')
            valid_input = False
        if not len(form_dict.get('days')) > 0 :
            flash('How many days is your trip?', 'days')
            valid_input = False
        if not form_dict.get('date'):
            flash("Please include trip's Start Date", 'date')
            valid_input = False
        return valid_input