from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

from db import items, db
from schemas import ItemSchema, ItemUpdateSchema
from models.item import Item
blp = Blueprint("items", __name__, description="Operations on items")

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return item
    def put(self, item_id, item_data):
        item = Item.query.get(item_id)
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = Item(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get('is_admin'):
            abort(401, message="You are not an admin.")
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()

        return {"message": 'Item deleted successfully.'}

    
@blp.route('/items')
class ItemList(MethodView):
    @blp.response(200, ItemUpdateSchema(many=True))
    def get(self):
        return list(items.values())
    @jwt_required(fresh=True)
    @blp.arguments(ItemUpdateSchema)
    @blp.response(201, ItemUpdateSchema)
    def post(self, item_data):
        item = Item(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(404, message=str(e))
        return item
