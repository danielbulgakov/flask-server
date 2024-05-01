from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError, JWTDecodeError
from datetime import timedelta
from api.common.register_routes import register_common_blueprints
from database.db import init_db

app = Flask(__name__)

# Register JWT
app.config['JWT_SECRET_KEY'] = 's3cr3t_k3y_f0r_jwt'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
jwt = JWTManager(app)

# Handle JWT exceptions
@app.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return jsonify({"msg": "Missing authorization header"}), 401

@app.errorhandler(InvalidHeaderError)
def handle_invalid_header_error(e):
    return jsonify({"msg": "Invalid authorization header"}), 401

@app.errorhandler(JWTDecodeError)
def handle_expired_signature_error(e):
    return jsonify({"msg": "Token has expired"}), 401

# Register blueprints
def register_blueprints(app):
    register_common_blueprints(app)

# Init dependency modules
register_blueprints(app)

# Init db
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://root:root@postgres:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app)

# DONT forget to remove
@app.route('/')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
