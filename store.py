import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import stores, db
from schemas import StoreSchema
from models.store import Store



blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route('/store/<string:store_id>')
class StoreView(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = Store.query.get_or_404(store_id)

        return store

    def delete(self, store_id):
        store = Store.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return "", 204

@blp.route('/stores')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        store = Store.query.all()
        return store

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        new_store = Store(**store_data)

        try:
            db.session.add(new_store)

            db.session.commit()
        except SQLAlchemyError as e:
            abort(404, message=str(e))

        return new_store
