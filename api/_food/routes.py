from flask import Flask, json, jsonify, request
from app import app
from food.models import Recipe, db


@app.route("/recipes", methods=['GET'])
def index():
    recipes = Recipe.query.all()
    return  jsonify([(Recipe.schema(recipe)) for recipe in recipes ])

@app.route("/create/recipe", methods=['POST'])
def create():
    data = json.loads(request.data)
    recipe = Recipe(
            title=data['title'],
            body = data['body'])
    db.session.add(recipe)
    db.session.commit()
    return  {'201' : 'recipe created successfully'}

@app.route('/recipe/<int:id>')
def showRecipe(id):
    recipes = Recipe.query.filter_by(id=id)
    return jsonify([Recipe.schema(recipe) for recipe in recipes])
