from flask import Blueprint, jsonify, request
from models import Petition

api = Blueprint('api', __name__, url_prefix='/slpp')

@api.route('/petitions', methods=['GET'])
def get_petitions():
    status = request.args.get('status')
    if status:
        petitions = Petition.query.filter_by(status=status).all()
    else:
        petitions = Petition.query.all()

    petitions_list = [
        {
            "petition_id": petition.petition_id,
            "status": petition.status,
            "petition_title": petition.title,
            "petition_text": petition.content,
            "petitioner": petition.petitioner_email,
            "signatures": petition.signature_count,
            "response": petition.response or "No response yet"
        }
        for petition in petitions
    ]

    return jsonify({"petitions": petitions_list})
