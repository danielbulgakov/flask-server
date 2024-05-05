from flask import Blueprint, request, jsonify
from database.db import ecg_data, ai_analysis

electron_bp = Blueprint('electron', __name__)

@electron_bp.route('/upload_ecg', methods=['POST'])
def upload_ecg():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # Get ECG data from the request
    ecg_data = request.json.get('ecg_data')

    if not ecg_data:
        return jsonify({"msg": "Missing ECG data"}), 400

    # Save ECG data to the database
    new_ecg_record = ecg_data(ecg_data=ecg_data)
    new_ecg_record.save()

    return jsonify({"msg": "ECG data uploaded successfully"}), 200

@electron_bp.route('/analyze_ecg', methods=['POST'])
def analyze_ecg():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # Get ECG data from the request
    ecg_data = request.json.get('ecg_data')

    if not ecg_data:
        return jsonify({"msg": "Missing ECG data"}), 400

    # Analyze ECG data using artificial intelligence
    analysis_result = ai_analysis.analyze_ecg(ecg_data)

    return jsonify({"analysis_result": analysis_result}), 200
