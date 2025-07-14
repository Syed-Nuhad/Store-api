from db import db

class Store(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    items = db.relationship('Item', back_populates='store', lazy='dynamic', cascade="all, delete, delete-orphan")
    tags = db.relationship('Tag', back_populates='store', lazy='dynamic')

    def __init__(self, name):
        self.name = name