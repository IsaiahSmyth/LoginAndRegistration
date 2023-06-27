from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = 'login_db'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(new_user):
        is_valid = True
        if len(new_user['first_name']) < 3:
            flash('First name must be at least 3 characters long')
            is_valid = False
        if not EMAIL_REGEX.match(new_user['email']):
            flash('Please enter a valid email')
            is_valid = False
        if len(new_user['last_name']) <4:
            flash('Last name must be at least 4 characters long')
            is_valid = False
        if len(new_user['password']) <6:
            flash('Last password must be at least 6 characters long')
            is_valid = False
        if new_user['password'] != new_user['confirm_password']:
            flash('passwords did not match!')
            is_valid = False

        return is_valid
    
    @classmethod
    def login_user(cls, current_user):
        is_valid = True
        if not EMAIL_REGEX.match(current_user['email']):
            flash('Please enter a valid email')
            is_valid = False
        
        user = cls.GetUserByEmail(current_user)
        if not user:
            flash('invalid email or password')
            is_valid = False
        elif not user.password == current_user['password']:
            flash('invalid email or password')
            is_valid = False
        return is_valid

    @classmethod
    def get_all(cls, data):
        query = """SELECT * FROM user"""

        results = connectToMySQL(cls.DB).query_db(query, data)
        all_regis = []
        for regis in results:
            all_regis.append(cls(regis))
        return all_regis

    @classmethod
    def Create_user(cls, data):
        query = """INSERT INTO user (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s );"""

        results = connectToMySQL(cls.DB).query_db(query, data)
        return results
    
    @classmethod
    def GetUserById(cls, data):
        query = """SELECT * FROM user WHERE id = %(id)s;"""

        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def GetUserByEmail(cls, data):
        query = """SELECT * FROM user WHERE email = %(email)s;"""

        results = connectToMySQL(cls.DB).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
