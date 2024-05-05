from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database.db import Users  # Assuming "Users" is the name of your table model

web_bp = Blueprint('web', __name__)

@web_bp.route('/update_profile', methods=['POST'])
def update_profile():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # Get data from the request
    login = request.json.get('login')
    birthdate = request.json.get('birthdate')

    if not login or not birthdate:
        return jsonify({"msg": "Missing login or birthdate"}), 400

    # Update user profile in the database
    user = Users.query.filter_by(login=login).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    user.birthdate = birthdate  # Assuming "birthdate" is a column in your Users table
    # You can add more fields to update here as needed

    # Commit changes to the database
    db.session.commit()

    return jsonify({"msg": "Profile updated successfully"}), 200

@web_bp.route('/view_ecg', methods=['GET'])
def view_ecg():
    # Get the current user from JWT
    current_user = get_jwt_identity()

    # Get ECG data from the database
    ecg_data = ecg_data.get_user_ecg_data(current_user)

    if not ecg_data:
        return jsonify({"msg": "No ECG data found"}), 404

    # Send ECG data in the response
    return jsonify({"ecg_data": ecg_data}), 200

@web_bp.route('/health_analysis', methods=['GET'])
def health_analysis():
    # Get the current user from JWT
    current_user = get_jwt_identity()

    # Get ECG data from the database
    ecg_data = ecg_data.get_user_ecg_data(current_user)

    if not ecg_data:
        return jsonify({"msg": "No ECG data found"}), 404

    # Analyze ECG data using artificial intelligence
    health_result = ai_analysis.analyze_ecg_data(ecg_data)

    # Send health analysis result in the response
    return jsonify({"health_analysis": health_result}), 200