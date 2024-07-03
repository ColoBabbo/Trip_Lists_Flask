from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d).+$')

class User:
    db = 'trip_lists_flask_db'

    def __init__(self, data:dict) -> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.recipes = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        all_users = []
        for user in results:
            all_users.append(cls(user))
        return all_users

    @classmethod
    def get_one(cls, user_id:int) -> object:
        query = """
                SELECT * FROM users
                WHERE id = %(id)s;
        """
        results = connectToMySQL(cls.db).query_db(query, {'id': user_id})
        return cls(results[0])

    @classmethod
    def update_one(cls, user_id:int) -> None:
        query = """
                UPDATE users
                SET first_name = %(first_name)s, last_name = %(last_name)s, 
                    email = %(email)s
                WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, {'id': user_id})

    @classmethod
    def insert_one(cls, form_dict:dict) -> int:
        query = """
                INSERT INTO users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(cls.db).query_db(query, form_dict)

    @classmethod
    def get_one_by_email(cls, this_email:str) -> object:
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;"""
        result = connectToMySQL(cls.db).query_db(query, {"email": this_email})
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_password_by_email(cls, this_email:str) -> object:
        query = """
                SELECT * FROM users
                WHERE email = %(email)s;"""
        result = connectToMySQL(cls.db).query_db(query, {"email": this_email})
        if len(result) < 1:
            return False
        return result[0]['password']

    @classmethod
    def get_user_if_login_legit(cls, form_data:dict) -> object:
        valid_input = True
        if not EMAIL_REGEX.match(form_data['email']): 
            flash('Email and password do not match!', 'login')
            return False
        user_in_db = cls.get_one_by_email(form_data.get('email'))
        if not user_in_db:
            flash('Email and password do not match!', 'login')
            return False
        if not bcrypt.check_password_hash(cls.get_password_by_email(form_data.get('email')), form_data['password']):
            flash('Email and password do not match!', 'login')
            return False
        return user_in_db

    @classmethod
    def is_legit_registration(cls, form_dict:dict) -> bool:
        valid_input = True
        if not len(form_dict.get('first_name')) > 0 :
            flash('Please enter your First Name.', 'first')
            valid_input = False
        elif not len(form_dict.get('first_name')) >= 2:
            flash('First Name must be at least 2 characters.', 'first')
            valid_input = False
        if not len(form_dict.get('last_name')) > 0 :
            flash('Please enter your Last Name.', 'last')
            valid_input = False
        elif not len(form_dict.get('last_name')) >= 2:
            flash('Last Name must be at least 2 characters.', 'last')
            valid_input = False
        if not EMAIL_REGEX.match(form_dict['email']):
            flash(f'Please enter a valid email address.', 'email')
            valid_input = False
        if cls.get_one_by_email(form_dict.get('email')):
            flash(f'Email address in use.', 'email')
            valid_input = False
        if not len(form_dict.get('password')) > 0 :
            flash('Please enter a Password.', 'pass')
            valid_input = False
        elif not len(form_dict.get('password')) >= 8:
            flash('Password must be at least 8 characters.', 'pass')
            valid_input = False
        if not PASS_REGEX.match(form_dict['password']):
            flash(f'Password must contain at least one number and one Uppercase letter.', 'pass')
            valid_input = False
        if form_dict.get('password') != form_dict.get('confirm_password'):
            flash(f'Passwords must match!', 'pass')
            valid_input = False
        return valid_input