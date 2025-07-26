import redis
import os

from flask import Flask, jsonify
from flask_smorest import Api

from db import db
from flask_migrate import Migrate


from item import blp as ItemBlueprint
from store import blp as StoreBlueprint
from tag import blp as TagBlueprint
from user import blp as UserBlueprint
from rq import Queue

from flask_jwt_extended import JWTManager
from blocklist import BLOCKLIST




app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = "SYED_CLEFERY_POKEMON_FUUU_BLACKBUYHADATROUBLEIHAVEWATERMELONINSTEAD"
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"  # Mount at root
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"  # Swagger at /swagger-ui
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  # Correct CDN
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


connection = redis.from_url(os.getenv("REDIS_URL"))
app.queue = Queue(connection=connection)
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)



@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {'is_admin': True}
    return {'is_admin': False}
api.register_blueprint(ItemBlueprint)
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST

@jwt.revoked_token_loader
def revoked_token(jwt_header, jwt_payload):
    return jsonify({'message': 'The token is no longer valid.'}), 401
@jwt.needs_fresh_token_loader
def fresh_token_loader(jwt_header, jwt_payload):
    return jsonify({'message': 'The token is no longer valid.'}), 401



api.register_blueprint(StoreBlueprint)
api.register_blueprint(TagBlueprint)
api.register_blueprint(UserBlueprint)



#font name= Elza Condensed

# 123upstashnuh!@#
# flask db upgrade docker compose up -d docker compose exec web flask db upgrade
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

