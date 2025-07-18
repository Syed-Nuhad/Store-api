from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from db import db
from blocklist import BLOCKLIST

from item import blp as ItemBlueprint
from store import blp as StoreBlueprint
from tag import blp as TagBlueprint
from user import blp as UserBlueprint

import models  # Ensures SQLAlchemy models are registered


app = Flask(__name__)

# ========== CONFIG ==========
app.config["JWT_SECRET_KEY"] = "SYED_CLEFERY_POKEMON_FUUU_BLACKBUYHADATROUBLEIHAVEWATERMELONINSTEAD"
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ========== EXTENSIONS ==========
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

# ========== JWT CALLBACKS ==========
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    return {"is_admin": identity == 1}

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token(jwt_header, jwt_payload):
    return jsonify({"message": "The token has been revoked."}), 401

@jwt.needs_fresh_token_loader
def fresh_token_required(jwt_header, jwt_payload):
    return jsonify({"message": "Fresh token required."}), 401

@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    return jsonify({"message": "The token has expired."}), 401

@jwt.invalid_token_loader
def invalid_token(error):
    return jsonify({"message": "Invalid token signature."}), 401

@jwt.unauthorized_loader
def missing_token(error):
    return jsonify({"message": "Token is missing from the request."}), 401

# ========== BLUEPRINTS ==========
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)
api.register_blueprint(TagBlueprint)
api.register_blueprint(UserBlueprint)

# ========== OPTIONAL: FOR DEV ==========
@app.before_first_request
def create_tables():
    db.create_all()

# ========== RUN APP ==========
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")