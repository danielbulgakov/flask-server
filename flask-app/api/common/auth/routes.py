from flask import Blueprint, request, jsonify
from database.db import auth, DBStatus

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

    return jsonify({"msg": "Login successful"}), 200

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

    new_auth_record = auth(login=login, password=password, email=email)
    status = new_auth_record.create()

    if status == DBStatus.OK:
        return jsonify({"msg": "Registration successful"}), 201
    else:
        return jsonify({"msg": "Failed to register user"}), 500

""" REMOVE """
@common_auth_bp.route('/users', methods=['GET'])
def get_all_users():
    users, status = users.return_all()

    if status == DBStatus.OK:
        user_data = [{"id": user.id, "full_name": user.full_name, "email": user.auth.email} for user in users]
        return jsonify({"users": user_data}), 200
    else:
        return jsonify({"msg": "Failed to fetch users"}), 500





