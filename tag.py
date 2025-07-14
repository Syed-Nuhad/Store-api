from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
from schemas import TagSchema, ItemsAndTagSchema
from models import Store, Item, Tag



blp = Blueprint("tags", __name__, description="Operations on tags")

@blp.route('/store/<string:store_id>/tag')
class Tags(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = Store.query.get_or_404(store_id)

        return store.tags.all()




    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema(many=True))

    def post(self, tag_data, store_id):
        store = Store(**tag_data, store_id=store_id)
        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, e)

        return "", 204

@blp.route('/tag/<string:tag_id>/item/<string:item_id>')
class LinkTagToItem(MethodView):
    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema(many=True))
    def get(self, tag_id, item_id):
        tag = Tag.query.get_or_404(tag_id)
        item = Item.query.get_or_404(tag_id)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError as e:
            abort(400, e)
        return tag

    @blp.response(200, ItemsAndTagSchema)
    def delete(self, tag_id, item_id):
        tag = Tag.query.get_or_404(tag_id)
        item = Item.query.get_or_404(tag_id)
        item.tags.remove(tag)
        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, e)
        return "Deletion successful", 204

@blp.route('/tag/<string:tag_id>')
class Tag(MethodView):
    @blp.arguments(TagSchema)
    @blp.response(200, TagSchema(many=True))
    def get(self, tag_id):
        tag = Tag.query.get_or_404(tag_id)
        return tag

    @blp.response(
        200,
                  description="Deletes a tag if no item  is tagged with it ",
                  example={"message": "Deleted tag"},
                  )
    @blp.alt_response(404, description="Tag not found")
    @blp.alt_response(400, description="Returned if the Tag is not associated with an item, the tag will not be deleted")
    def delete(self, tag_id, item_id):
        tag = Tag.query.get_or_404(tag_id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return "{'message': 'tag deleted'}", 204
        return abort(400, description="Cant delete tag because it is not associated with an item")