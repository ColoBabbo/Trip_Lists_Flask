from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import trip, item

class List:
    db = 'trip_lists_flask_db'

    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.name = data['name']
        self.trip_id = data['trip_id']
        self.trip = {}
        self.items = []

    def __repr__(self) -> str:
        return f'List & id: {self.name} {self.id}, \n Items: {self.items}'

    @classmethod
    def get_all (cls):
        query = """
                SELECT * FROM lists
                LEFT JOIN trips ON lists.trip_id = trips.id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        all_lists = []
        for list in results:
            this_list = cls(list)
            trip_data = {
                'id': list['trips.id'],
                'name': list['name'],
                'location': list['location'],
                'date': list['date'],
            }
            this_list_trip = trip.Trip(trip_data)
            this_list.trip = this_list_trip
            all_lists.append(this_list)
        return all_lists


    @classmethod
    def insert_one(cls, form_dict:dict) -> int:
        query = """
                INSERT INTO lists (name, trip_id)
                VALUES (%(name)s, %(trip_id)s);
        """
        data = {
            'name': form_dict['list_name'],
            'trip_id': form_dict['trip_id'],
        }
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def is_legit_list(cls, form_dict:dict) -> bool:
        valid_input = True
        if not len(form_dict.get('list_name')) > 0 :
            flash('Your list needs a name!', 'list_name')
            valid_input = False
        elif not len(form_dict.get('list_name')) >= 3:
            flash('Name must be at least 3 characters.', 'list_name')
            valid_input = False
        return valid_input

    @classmethod
    def delete_one(cls, list_id:int) -> None:
        query = """
                DELETE FROM lists
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {"id": list_id})

    @classmethod
    def update_one(cls, form_dict:dict) -> None:
        query = """
                UPDATE lists
                SET name = %(name)s, trip_id =  %(trip_id)s
                WHERE id = %(list_id)s;
        """
        return connectToMySQL(cls.db).query_db(query, form_dict)