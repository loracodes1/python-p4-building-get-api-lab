#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    # Get all bakeries and their baked goods
    bakeries = Bakery.query.all()
    return jsonify([bakery.to_dict() for bakery in bakeries])

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # Get a bakery by ID with its baked goods
    bakery = Bakery.query.get(id)
    if bakery:
        return jsonify(bakery.to_dict())
    return jsonify({"error": "Bakery not found"}), 404

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # Get baked goods sorted by price in descending order
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return jsonify([baked_good.to_dict() for baked_good in baked_goods])

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # Get the most expensive baked good
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        return jsonify(baked_good.to_dict())
    return jsonify({"error": "No baked goods found"}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
