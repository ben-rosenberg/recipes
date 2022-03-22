from flask_app import app
from flask_app.controllers import controller_routes, controller_recipe, controller_user

if __name__ == '__main__':
    app.run(debug = True)