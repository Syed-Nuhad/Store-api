import os

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, get_jwt, create_refresh_token, jwt_required, get_jwt_identity
from flask import current_app

from db import stores, db
from models.user import User
from blocklist import BLOCKLIST
from sqlalchemy import or_



from passlib.hash import pbkdf2_sha256
from schemas import UserSchema, UserRegisterSchema


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

blp = Blueprint("Users", "users", __name__, description="Operations on users")



def send_email(to_email, subject, body):


    msg = MIMEMultipart()
    msg["From"] = "nuhad7july0@gmail.com"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("nuhad7july0@gmail.com", "duva valh ttda ffye")
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()
        print("✅ Email sent successfully")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def send_registration_email( *, username, email):
    print(f"📧 Sending registration email to: {username}, {email}")
    return send_email(to_email=email, subject="Hi there! You Succesfully signed up.", body=f"Hi {username} you have succesfully registered to stores REST API !")



@blp.route("/register")
class Register(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if User.query.filter(or_(User.username == user_data["username"]), User.email == user_data["email"]).first():
            abort(409, message="Username already exists")

        # Create user
        user = User(username=user_data["username"], email=user_data["email"], password=pbkdf2_sha256.hash(user_data["password"]))
        db.session.add(user)
        db.session.commit()

        current_app.queue.enqueue_call(
            func=send_registration_email,
            args=(user.username, user.email),
            queue_name="emails"
        )



        # Generate tokens
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
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {'message': 'User logged out'}, 200





