from flask import Blueprint, request, jsonify
from services.band6 import band6_data

band6_bp = Blueprint('band6', __name__)

@band6_bp.route('/band6', methods=['POST'])
def get_band6():
    data = request.get_json()
    school_name = data.get('school')

    if not school_name:
        return jsonify({'error': 'Missing school name'}), 400

    school_data = band6_data.get(school_name)

    if not school_data:
        return jsonify({'error': 'School not found'}), 404

    return jsonify({'school_data': school_data})

@band6_bp.route('/band6/schools', methods=['GET'])
def schools():
    schools = list(band6_data.keys())

    if not schools:
        return jsonify({'error': 'Schools list not found'}), 404

    return jsonify({'schools': schools})