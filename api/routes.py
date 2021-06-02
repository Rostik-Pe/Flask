from flask_restful import Resource
from flask import request

from api.services.item_service import ItemService
from market import api
from typing import List
from market import db
from market.models import Item, User


class Smoke(Resource):
    def get(self):
        return {'message': 'OK'}, 200


class ItemListApi(Resource):
    def get(self, id=None):
        if not id:
            items = ItemService.fetch_all_items(db.session)
            # items = db.session.query(Item).all()
            return [i.to_dict() for i in items], 200
        # item = db.session.query(Item).filter_by(id=id).first()
        item = ItemService.fetch_item_by_id(db.session, id)
        if not item:
            return '', 404
        return item.to_dict(), 200

    def post(self):
        item_json = request.json
        if not item_json:
            return {'message': 'Wrong data'}
        try:
            item = Item(
                name=item_json['name'],
                price=item_json['price'],
                barcode=item_json['barcode'],
                description=item_json['description']
            )
            db.session.add(item)
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Created Successfully!'}, 201

    def put(self, id):
        # item_json = request.json
        item = ItemService.fetch_item_by_id(db.session, id)
        if not item:
            return {'message': 'Wrong data'}, 400
        try:
            db.session.query(Item).filter_by(id=id).update(
                dict(
                    name=item.get('name'),
                    price=item.get('price'),
                    barcode=item.get('barcode'),
                    description=item.get('description')
                )
            )
            db.session.commit()
        except (ValueError, KeyError):
            return {'message': 'Wrong data'}, 400
        return {'message': 'Updated Successfully!'}, 200

    def delete(self, id):
        # item = db.session.query(Item).filter_by(id=id).first()
        item = ItemService.fetch_item_by_id(db.session, id)
        if not item:
            return '', 404
        db.session.delete(item)
        db.session.commit()
        return '', 204

class UserListApi(Resource):
    def get(self, id=None):
        if not id:
            user = db.session.query(User).all()
            return [u.to_dict() for u in user], 200
        user = db.session.query(User).filter_by(id=id).first()
        if not user:
            return '', 404
        return user.to_dict(), 200

api.add_resource(Smoke, '/smoke', strict_slashes=False)  # strict_slashes - /smoke/ will work
api.add_resource(ItemListApi, '/items', '/items/<id>', strict_slashes=False)
api.add_resource(UserListApi, '/users', '/users/<id>', strict_slashes=False)
# def patch(self, id):
#     item = db.session.query(Item).filter_by(id=id).first()
#     if not item:
#         return '', 404
#     item_json = request.json
#     name = item_json.get('name')
#     price = item_json.get('price')
#     barcode = item_json.get('barcode')
#     description = item_json('description')
#     if name:
#         item.name = name
#     elif price:
#         item.price = price
#     elif barcode:
#         item.barcode = barcode
#     elif description:
#         item.description = description
#     db.session.add(item)
#     db.session.commit()
#     return {'message': 'Updated successfully1'}, 200
