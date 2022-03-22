from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe
from flask_app import app, render_template, redirect, request, session


@app.route('/validate_login', methods=['POST'])
def validate_login():
    is_valid = User.validate_user_login(request.form)
    if not is_valid:
        return redirect('/')
    return redirect('/dashboard')

@app.route('/validate_registration', methods=['POST'])
def validate_registration():
    if not User.validate_user_registration(request.form):
        return redirect('/')
    session['user_id'] = User.create_user(request.form)
    return redirect('/dashboard')
    
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: # might need to be if not 'user_id' in session
        return redirect('/')
    this_user = User.get_user_by_id(session['user_id'])
    all_recipes_with_names = Recipe.get_all_recipes_with_user_names()
    return render_template('dashboard.html', user=this_user, all_recipes=all_recipes_with_names)

@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/')