from flask import Blueprint, request, jsonify
from services.polynomial import load_subjects

predict_bp = Blueprint('predict', __name__)

@predict_bp.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    subject_name = data.get('subject')
    raw_mark = data.get('rawMark')

    if not subject_name or raw_mark is None:
        return jsonify({'error': 'Missing subject name or raw mark'}), 400

    subject = load_subjects(subject_name).get(subject_name)

    print(subject)

    if not subject:
        return jsonify({'error': 'Subject not found'}), 404

    predictions = []

    for years, marks in subject.items():
        if "polynomial" in marks and marks["polynomial"] is not None:
            predicted_mark = marks["polynomial"](raw_mark)
            predictions.append({'year': years, 'predicted_mark': round(predicted_mark, 2)})

    return jsonify({'predictions': predictions})