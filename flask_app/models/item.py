from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import trip

class Item:
    db = 'trip_lists_flask_db'

    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.name = data['name']
        self.unit = data['unit']
        self.quantity = data['quantity']
        # self.is_packed = data['is_packed']
        self.list_id = data['list_id']

    def __repr__(self) -> str:
        return f'Item: {self.name}'

    @classmethod
    def insert_one(cls, form_dict:dict) -> int:
        query = """
                INSERT INTO items (name, unit, quantity, list_id)
                VALUES (%(name)s, %(unit)s, %(quantity)s, %(list_id)s);
        """
        return connectToMySQL(cls.db).query_db(query, form_dict)

    @classmethod
    def is_legit_item(cls, form_dict:dict) -> bool:
        valid_input = True
        if not len(form_dict.get('name')) > 0 :
            flash('Your item needs a name!', 'name')
            valid_input = False
        elif not len(form_dict.get('name')) >= 3:
            flash('Idem Name must be at least 3 characters.', 'name')
            valid_input = False
        return valid_input