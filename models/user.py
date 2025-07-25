import email

from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.email = email
        self.password = password