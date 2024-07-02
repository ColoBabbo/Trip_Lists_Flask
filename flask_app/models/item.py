from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

class Item:
    db = 'trip_lists_flask_db'

    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.name = data['name']
        self.unit = data['unit']
        self.quantity = data['quantity']
        self.is_packed = data['is_packed']
        self.list_id = data['list_id']
        self.list_name = None
        self.user_id = None

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
            flash('Item Name must be at least 3 characters.', 'name')
            valid_input = False
        if not float(form_dict.get('quantity')) > 0:
            flash('Quantity must be greater than 0.', 'quantity')
            valid_input = False
        return valid_input

    @classmethod
    def get_one(cls, item_id:int) -> object:
        query = """
                SELECT * FROM items
                LEFT JOIN lists ON items.list_id = lists.id
                LEFT JOIN trips ON lists.trip_id = trips.id
                LEFT JOIN users ON users.id = trips.user_id
                WHERE items.id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'id': item_id})
        if results:
            this_result = results[0]
            this_item = cls(this_result)
            this_item.list_name = this_result['lists.name']
            this_item.user_id = this_result['users.id']
            return this_item
        else:
            return False

    @classmethod
    def delete_one(cls, item_id:int) -> None:
        query = """
                DELETE FROM items
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {"id": item_id})

    @classmethod
    def update_one_json(cls, form_dict:dict) -> None:
        query = """
                UPDATE items
                SET name = %(name)s, unit =  %(unit)s, quantity = %(quantity)s, is_packed = %(is_packed)s
                WHERE id = %(item_id)s;
        """
        data = {
            'name': form_dict['name'],
            'unit': form_dict['unit'],
            'quantity': form_dict['quantity'],
            'is_packed': (1 if form_dict['is_packed'] == 'true' else 0),
            'item_id': form_dict['item_id'],
        }
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_one(cls, form_dict:dict) -> None:
        query = """
                UPDATE items
                SET name = %(name)s, unit =  %(unit)s, quantity = %(quantity)s, is_packed = %(is_packed)s
                WHERE id = %(item_id)s;
        """
        data = {
            'name': form_dict['name'],
            'unit': form_dict['unit'],
            'quantity': form_dict['quantity'],
            'is_packed': (1 if form_dict.get('is_packed') else 0),
            'item_id': form_dict['item_id'],
        }
        return connectToMySQL(cls.db).query_db(query, data)
