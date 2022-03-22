from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATE_REGEX, DATABASE, DATE_REGEX
from flask import flash


class Recipe:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30 = data['under_30']
        self.origin_date = data['origin_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
    
    @classmethod
    def get_all_recipes(cls) -> list:
        query = 'SELECT * FROM recipes;'
        query_results = connectToMySQL(DATABASE).query_db(query)
        if not query_results:
            return []
        all_recipes = []
        for result in query_results:
            all_recipes.append(cls(result))
        return all_recipes        

    @classmethod
    def get_all_recipes_with_user_names(cls):
        query = 'SELECT recipes.*, users.first_name, users.last_name FROM recipes \
            JOIN users ON recipes.user_id = users.id;'
        query_results = connectToMySQL(DATABASE).query_db(query)
        if not query_results:
            return []
        all_recipes_with_names = []
        for result in query_results:
            this_recipe = cls(result)
            this_recipe.first_name = result['first_name']
            this_recipe.last_name = result['last_name']
            all_recipes_with_names.append(this_recipe)
        return all_recipes_with_names

    @classmethod
    def get_recipe_by_id(cls, recipe_id: str) -> 'Recipe':
        data = { 'id': recipe_id }
        query = 'SELECT * FROM recipes \
            WHERE id = %(id)s;'
        query_results = connectToMySQL(DATABASE).query_db(query, data)
        if not query_results:
            return None
        return cls(query_results[0])

    @classmethod
    def get_recipe_by_id_with_name(cls, recipe_id):
        data = { 'id': recipe_id }
        query = 'SELECT recipes.*, users.first_name, users.last_name \
            FROM recipes \
            JOIN users ON recipes.user_id = users.id \
            WHERE recipes.id = %(id)s;'
        query_results = connectToMySQL(DATABASE).query_db(query, data)
        if not query_results:
            return []
        this_recipe_instance = cls(query_results[0])
        this_recipe_instance.first_name = query_results[0]['first_name']
        this_recipe_instance.last_name = query_results[0]['last_name']
        return this_recipe_instance
        

    @classmethod
    def create_recipe(cls, form_data: dict, user_id: str) -> int:
        data = {
            **form_data,
            'user_id': user_id
        }
        query = 'INSERT INTO recipes \
            (name, description, instructions, under_30, origin_date, user_id) \
            VALUES(%(name)s, %(description)s, %(instructions)s, \
            %(under_30)s, %(origin_date)s, %(user_id)s);'
        new_recipe_id = connectToMySQL(DATABASE).query_db(query, data)
        return new_recipe_id

    @classmethod
    def update_recipe(cls, recipe_id, form_data) -> None:
        data = {
            **form_data,
            'recipe_id': recipe_id
        }
        query = 'UPDATE recipes \
            SET name = %(name)s, \
            description = %(description)s, \
            instructions = %(instructions)s, \
            under_30 = %(under_30)s, \
            origin_date = %(origin_date)s \
            WHERE id = %(recipe_id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return None

    @classmethod
    def delete_recipe(cls, recipe_id) -> None:
        data = {
            'id': recipe_id
        }
        query = 'DELETE FROM recipes \
            WHERE id = %(id)s;'
        connectToMySQL(DATABASE).query_db(query, data)
        return None

    @staticmethod
    def validate_recipe(form_data) -> bool:
        is_valid = True
        if len(form_data['name']) == 0:
            is_valid = False
            flash('Recipe name field must not be empty', 'error_recipe_name')
        elif len(form_data['name']) < 4:
            is_valid = False
            flash('Recipe name must be at least 3 characters long', 'error_recipe_name')
        if len(form_data['description']) == 0:
            is_valid = False
            flash('Recipe description field must not be empty', 'error_recipe_description')
        elif len(form_data['description']) < 4:
            is_valid = False
            flash('Recipe description must be at least 3 characters long', 'error_recipe_description')
        if len(form_data['instructions']) == 0:
            is_valid = False
            flash('Recipe instructions field must not be empty', 'error_recipe_instructions')
        elif len(form_data['instructions']) < 4:
            is_valid = False
            flash('Recipe instructions must be at least 3 characters long', 'error_recipe_instructions')
        if len(form_data['origin_date']) == 0:
            is_valid = False
            flash('Recipe date field must not be empty', 'error_recipe_origin_date')
        elif not DATE_REGEX.match(form_data['origin_date']):
            is_valid = False
            flash('Invalid recipe date format, must be: YYYY-MM-DD', 'error_recipe_origin_date')
        return is_valid