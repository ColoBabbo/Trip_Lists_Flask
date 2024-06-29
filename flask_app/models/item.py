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
        self.list_id = data['list_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
