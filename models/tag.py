from db import db

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("Store", back_populates="tags")

    # ✅ Rename 'item' to 'items' and match back_populates
    items = db.relationship("Item", secondary="item_tags", back_populates="tags")

