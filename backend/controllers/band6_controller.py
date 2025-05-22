from flask import Blueprint, request, jsonify
from supabase_client.client import supabase

band6_bp = Blueprint('band6', __name__)

@band6_bp.route('/band6', methods=['POST'])
def get_band6():
    data = request.get_json()
    school_name = data.get('school')

    if not school_name:
        return jsonify({'error': 'Missing school name'}), 400

    response = supabase.table("Band 6 Data").select("*").eq("school", school_name).execute()
    rows = response.data

    if not rows:
        return jsonify({'error': 'School not found'}), 404

    school_data = {}

    for row in rows:
        subject = row['subject']
        year = row['year']
        band6_count = row['num_band6']

        if subject not in school_data:
            school_data[subject] = {}

        if year not in school_data[subject]:
            school_data[subject][year] = 0

        school_data[subject][year] = band6_count

    return jsonify({'school_data': school_data})

@band6_bp.route('/band6/schools', methods=['GET'])
def schools():
    response = supabase.table("distinct_schools").select("school").execute()
    rows = response.data

    if not rows:
        return jsonify({'error': 'Schools list not found'}), 404

    schools = list(set(row['school'] for row in rows))

    return jsonify({'schools': schools})