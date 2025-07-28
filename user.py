import os
from tasks import send_registration_email

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from flask import current_app

from db import db
from models.user import User
from blocklist import BLOCKLIST
from sqlalchemy import or_
from passlib.hash import pbkdf2_sha256
from schemas import UserSchema, UserRegisterSchema


blp = Blueprint("Users", "users", __name__, description="Operations on users")


@blp.route("/register")
class Register(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if User.query.filter(
            or_(User.username == user_data["username"], User.email == user_data["email"])
        ).first():
            abort(409, message="Username or email already exists")

        # Create user
        user = User(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        # Enqueue email job correctly with keyword arguments
        job = current_app.queue.enqueue_call(
            func=send_registration_email,
            kwargs={"username": user.username, "email": user.email},
        )

        print(f"✅ Job enqueued: {job.id}")

        # Generate tokens
        access_token = create_access_token(identity=str(user.id), fresh=True)
        refresh_token = create_refresh_token(identity=str(user.id))

        return {
            "message": "User registered",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, 201


@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = User.query.filter(User.username == user_data["username"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.id), fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200
        abort(401, message="Invalid credentials")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=str(current_user), fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200


@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "User logged out"}, 200


