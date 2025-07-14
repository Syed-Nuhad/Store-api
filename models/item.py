from db import db

class Item(db.Model):
    __tablename__ = 'items'  # ✅ Correct table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    store = db.relationship("Store", back_populates="items")  # ✅ back to 'items'
