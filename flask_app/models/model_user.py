from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt, DATABASE, session, EMAIL_REGEX
from flask import flash


class User:
    def __init__(self, data: dict) -> None:
        self.id         = data['id']
        self.first_name = data['first_name']
        self.last_name  = data['last_name']
        self.email      = data['email']
        self.password   = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_user_by_id(cls, user_id: str) -> 'User':
        data = { 'id': user_id } # may need to cast to int
        query = 'SELECT * FROM users \
            WHERE id = %(id)s;'
        query_results: list[dict] = connectToMySQL(DATABASE).query_db(query, data)
        if not query_results:
            return None
        return cls(query_results[0])

    @classmethod
    def get_user_by_email(cls, email: str) -> 'User':
        data = { 'email': email }
        query = 'SELECT * FROM users \
            WHERE email = %(email)s;'
        query_results = connectToMySQL(DATABASE).query_db(query, data)
        if not query_results:
            return None
        return cls(query_results[0])

    '''
    Called after registration form has been submitted and validated. Rather
    than use the form's data, the password is hashed and combined with the
    rest of the form data.
    '''
    @classmethod
    def create_user(cls, form_data: dict) -> int:
        data_with_hashed_password = {
            **form_data,
            'password': bcrypt.generate_password_hash(form_data['password'])
        }
        query = 'INSERT INTO users (first_name, last_name, email, password) \
            VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        new_user_id = connectToMySQL(DATABASE).query_db(
            query, data_with_hashed_password)
        return new_user_id


    '''
    Checks validity of registration form input values. Returns false if any
    are true, and adds relevant error messages to flash.
    '''
    @staticmethod
    def validate_user_registration(form_data: dict) -> bool:
        is_valid = True
        if len(form_data['first_name']) == 0:
            is_valid = False
            flash(
                'First name field must not be empty',
                'error_users_first_name')
        elif len(form_data['first_name']) < 3:
            is_valid = False
            flash(
                'First name must have at least 2 characters',
                'error_users_first_name')
        elif not form_data['first_name'].isalpha():
            is_valid = False
            flash(
                'First name must only contain alphabetic characters', 
                'error_users_first_name')
        if len(form_data['last_name']) == 0:
            is_valid = False
            flash(
                'Last name field must not be empty',
                'error_users_last_name')
        elif len(form_data['last_name']) < 3:
            is_valid = False
            flash(
                'Last name must be greater than 2 characters',
                'error_users_last_name')
        elif not form_data['last_name'].isalpha():
            is_valid = False
            flash(
                'Last name must only contain alphabetic characters',
                'error_users_last_name')
        if len(form_data['email']) == 0:
            is_valid = False
            flash('Email field must not be empty', 'error_users_email')
        elif not EMAIL_REGEX.match(form_data['email']):
            is_valid = False
            flash('Incorrect email format', 'error_users_email')
        elif User.get_user_by_email(form_data['email']) is not None:
            is_valid = False
            flash(
                'Account with this email already exists',
                'error_users_email')
        if len(form_data['password']) == 0:
            is_valid = False
            flash('Password field must not be empty', 'error_users_password')
        elif len(form_data['password']) < 8:
            is_valid = False
            flash(
                'Password must have at least 8 characters',
                'error_users_password')
        if form_data['password'] != form_data['confirm_password']:
            is_valid = False
            flash('Passwords do not match', 'error_users_confirm_password')
        return is_valid
    
    '''
    Checks validity of login form input values. If valid and if email matches
    a record from the database, returns true and adds the user's ID to session.
    '''
    @staticmethod
    def validate_user_login(form_data: dict) -> bool:
        is_valid = True
        if len(form_data['email']) == 0:
            is_valid = False
            flash('Email field must not be empty', 'error_users_email_login')
        if len(form_data['password']) == 0:
            is_valid = False
            flash(
                'Password field must not be empty',
                'error_users_password_login')
        if is_valid:
            potential_user = User.get_user_by_email(form_data['email'])
            if potential_user == None:
                is_valid = False
                flash('Incorrect email or password', 'error_users_login')
            elif not bcrypt.check_password_hash(
                    potential_user.password, form_data['password']):
                is_valid = False
                flash('Incorrect email or password', 'error_users_login')
            else:
                session['user_id'] = potential_user.id
        return is_valid

        