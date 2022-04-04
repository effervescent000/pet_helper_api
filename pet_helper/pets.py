from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user

from .models import Pet
from .schema import PetSchema
from . import db

bp = Blueprint("pet", __name__, url_prefix="/pets")

one_pet_schema = PetSchema()
multi_pet_schema = PetSchema(many=True)


# GET endpoints


@bp.route("/", methods=["GET"])
@jwt_required()
def get_pets():
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    return jsonify(multi_pet_schema.dump(pets))


# POST endpoints
