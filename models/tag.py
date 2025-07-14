from db import db

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("Store", back_populates="tags")  # ✅ back to 'tags'
    item = db.relationship("Item", back_populates="tags", secondary="item_tags")

