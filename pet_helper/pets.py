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


@bp.route("/", methods=["POST"])
@jwt_required()
def add_pet():
    data = request.get_json()
    owner_id = current_user.id
    name = data.get("name")
    if not name:
        name = "Unnamed"
    type = data.get("type")
    if not type:
        return jsonify({"error": "no type included in request"}), 400
    species = data.get("species")
    if not species:
        species = "Unknown"
    weight = data.get("weight")
    feed_frequency = data.get("feed_frequency")
    notes = data.get("notes")

    pet = Pet(
        name=name,
        type=type,
        species=species,
        weight=weight,
        feed_frequency=feed_frequency,
        notes=notes,
        owner_id=owner_id,
    )
    db.session.add(pet)
    db.session.commit()
    return jsonify(one_pet_schema.dump(pet))
