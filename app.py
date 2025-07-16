
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gogobar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    archived = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    recipes = Recipe.query.filter_by(archived=False).all()
    return render_template('index.html', recipes=recipes)

@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    name = request.form['name']
    category = request.form['category']
    sale_price = float(request.form['sale_price'])
    new_recipe = Recipe(name=name, category=category, sale_price=sale_price)
    db.session.add(new_recipe)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/archive/<int:id>')
def archive(id):
    recipe = Recipe.query.get_or_404(id)
    recipe.archived = True
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
