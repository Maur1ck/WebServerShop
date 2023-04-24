from flask import jsonify
from flask_restful import Resource, reqparse
from data import db_session
from data.products import Product


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('description', required=True)
parser.add_argument('price', required=True, type=float)


class ProductResource(Resource):
    def get(self, product_id):
        db_sess = db_session.create_session()
        product = db_sess.query(Product).get(product_id)
        if not product:
            return {'error': 'Not found'}, 404
        return {'product': product.to_dict(only=('id', 'name', 'description', 'price'))}

    def delete(self, product_id):
        db_sess = db_session.create_session()
        product = db_sess.query(Product).get(product_id)
        if not product:
            return {'error': 'Not found'}, 404

        db_sess.delete(product)
        db_sess.commit()

        return {'success': 'Product deleted'}


class ProductListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        products = db_sess.query(Product).all()
        return jsonify([product.to_dict() for product in products])

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        product = Product(
            name=args['name'],
            description=args['description'],
            price=args['price'],
        )
        db_sess.add(product)
        db_sess.commit()
        return {'success': 'OK'}
