import uuid
from os import access

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, create_refresh_token, jwt_required, get_jwt_identity
from db import stores, db
from schemas import UserSchema
from models.user import User
from blocklist import BLOCKLIST


blp = Blueprint("Users", "users", __name__, description="Operations on users")
@blp.route("/register")
class Register(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if User.query.filter(User.username == user_data["username"]).first():
            abort(409, message="Username already exists")

        user = User(user_data["username"], pbkdf2_sha256.hash(user_data["password"]))
        db.session.add(user)
        db.session.commit()

        # Generate tokens after successful registration
        access_token = create_access_token(identity=str(user.id), fresh=True)
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            'message': 'User registered',
            'access_token': access_token,
            'refresh_token': refresh_token
        }, 201


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = User.query.filter(User.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(f'{user.id}', ), fresh=True)
            refresh_token = create_refresh_token(identity=str(f'{user.id}'))
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        abort(401, message="Invalid credentials")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=str(f'{current_user}', ), fresh=False)
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {'access_token': new_token}, 200



@blp.route("/logout")
class Logout(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {'message': 'User logged out'}, 200