from dataclasses import dataclass
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from producer import publish
import requests


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@db/main'
CORS(app)


db = SQLAlchemy(app)


@dataclass
class Product(db.Model):
    id: int
    sku: str
    name: str
    price: float
    brand: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    sku = db.Column(db.String(8))
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    brand = db.Column(db.String(100))
    image = db.Column(db.String(500))


@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return jsonify(Product.query.all())


@app.route('/api/products/<int:id>/views', methods=['POST'])
def views(id):
    req = requests.get('http://docker.for.linux.localhost:8000/api/user')
    json = req.json()
    productUser = ProductUser(user_id=json['id'], product_id=id)
    db.session.add(productUser)
    db.session.commit()
    publish('product_viewed', id)

    return jsonify({
        'message': 'success'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
