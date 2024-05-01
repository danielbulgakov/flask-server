from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from database.db import auth, DBStatus, users

common_auth_bp = Blueprint('auth', __name__)

@common_auth_bp.route('/login', methods=['POST'])
def login_post():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    login = request.json.get('login')
    password = request.json.get('password')

    if not login or not password:
        return jsonify({"msg": "Missing login or password"}), 400

    auth_record, status = auth.find_by_login(login)

    if status == DBStatus.ERROR or auth_record is None:
        return jsonify({"msg": "Invalid login credentials"}), 401

    if auth_record.password != password:
        return jsonify({"msg": "Invalid login credentials"}), 401

    access_token = create_access_token(identity=login)
    refresh_token = create_refresh_token(identity=login)
    return jsonify({"msg": "Login successful", "access_token": access_token, "refresh_token": refresh_token}), 200

@common_auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": access_token}), 200

@common_auth_bp.route('/register', methods=['POST'])
def register_post():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    login = request.json.get('login')
    password = request.json.get('password')
    email = request.json.get('email')

    if not login or not password or not email:
        return jsonify({"msg": "Missing required fields"}), 400

    existing_auth_record, status = auth.find_by_login(login)

    if status == DBStatus.OK and existing_auth_record:
        return jsonify({"msg": "Login already exists"}), 400

    existing_email_record, status = auth.find_by_email(email)

    if status == DBStatus.OK and existing_email_record:
        return jsonify({"msg": "Email already registered"}), 400
    
    new_user_record = users()
    status_user = new_user_record.create()
    
    if status_user != DBStatus.OK:
        return jsonify({"msg": "Failed to register user"}), 500

    new_auth_record = auth(login=login, password=password, email=email, user_id=new_user_record.id)
    status = new_auth_record.create()

    if status == DBStatus.OK:
        return jsonify({"msg": "Registration successful"}), 200
    else:
        return jsonify({"msg": "Failed to register user"}), 500

""" REMOVE """
@common_auth_bp.route('/auths', methods=['GET'])
def get_all_auths():
    from database.db import auth
    auths, status = auth.return_all()

    if status == DBStatus.OK:
        user_data = [{"id": auth.id, "login": auth.login, "email": auth.email, "id_user": auth.user_id} for auth in auths]
        return jsonify({"auths": user_data}), 200
    else:
        return jsonify({"msg": "Failed to fetch users"}), 500

""" REMOVE """
@common_auth_bp.route('/users', methods=['GET'])
def get_all_users():
    from database.db import users
    users, status = users.return_all()

    if status == DBStatus.OK:
        user_data = [{"id": users.id} for users in users]
        return jsonify({"users": user_data}), 200
    else:
        return jsonify({"msg": "Failed to fetch users"}), 500





