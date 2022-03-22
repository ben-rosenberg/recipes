from flask_app.models.model_recipe import Recipe
from flask_app.models.model_user import User
from flask_app import app, render_template, redirect, request, session


@app.route('/recipes/<recipe_id>')
def view_recipe(recipe_id: str) -> str:
    if not 'user_id' in session:
        return redirect('/')
    this_recipe_with_name = Recipe.get_recipe_by_id_with_name(recipe_id)
    if not this_recipe_with_name:
        return redirect('/')
    this_user = User.get_user_by_id(session['user_id'])
    return render_template('recipe.html', recipe=this_recipe_with_name, user=this_user)

@app.route('/recipes/new')
def new_recipe_form():
    if not 'user_id' in session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_new_recipe():
    if not 'user_id' in session:
        return redirect('/')
    new_recipe_id = Recipe.create_recipe(request.form, session['user_id'])
    return redirect(f'/recipes/{new_recipe_id})')

@app.route('/recipes/<recipe_id>/edit')
def edit_recipe(recipe_id: str):
    if not 'user_id' in session:
        return redirect('/')
    this_recipe = Recipe.get_recipe_by_id(recipe_id)
    if not this_recipe:
        return redirect('/')
    if this_recipe.user_id != session['user_id']: # Maybe flash message here: must be logged in as that user
        return redirect(f'/recipes/{recipe_id}')
    return render_template('edit_recipe.html', recipe=this_recipe)

@app.route('/recipes/<int:recipe_id>/update', methods=['POST'])
def update_recipe(recipe_id):
    this_recipe = Recipe.get_recipe_by_id(recipe_id)
    if this_recipe.user_id != session['user_id']: # Maybe flash message here: must be logged in as that user
        return redirect(f'/recipes/{recipe_id}')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/{recipe_id}/edit')
    Recipe.update_recipe(recipe_id, request.form)
    return redirect(f'/recipes/{recipe_id}')

@app.route('/recipes/<recipe_id>/delete')
def delete_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    this_recipe = Recipe.get_recipe_by_id(recipe_id)
    if session['user_id'] != this_recipe.user_id:
        return redirect('/')
    Recipe.delete_recipe(recipe_id)
    return redirect('/')