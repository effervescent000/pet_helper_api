from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user
from datetime import datetime

from .models import Pet
from .schema import PetSchema
from . import db
from .utils import time_format

bp = Blueprint("pet", __name__, url_prefix="/pets")

one_pet_schema = PetSchema()
multi_pet_schema = PetSchema(many=True)

# GET endpoints


@bp.route("/", methods=["GET"])
@jwt_required()
def get_pets():
    pets = Pet.query.filter_by(owner_id=current_user.id).all()
    return jsonify(multi_pet_schema.dump(pets))


@bp.route("/<id>", methods=["GET"])
@jwt_required()
def get_pet_by_id(id):
    pet = Pet.query.get(id)
    if pet:
        if pet.owner_id == current_user.id or current_user.role == "admin":
            return jsonify(one_pet_schema.dump(pet))
        return jsonify({"error": "not authorized"}), 401
    return jsonify({"error": "invalid pet"}), 400


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
    feed_frequency = data.get("feedFrequency")
    notes = data.get("notes")

    date_born = data.get("dateBorn")
    if date_born:
        date_born = datetime.strptime(date_born, time_format)
    date_acquired = data.get("dateAcquired")
    if date_acquired:
        date_acquired = datetime.strptime(date_acquired, time_format)
    date_removed = data.get("dateRemoved")
    if date_removed:
        date_removed = datetime.strptime(date_removed, time_format)
    date_fed = data.get("dateFed")
    if date_fed:
        date_fed = datetime.strptime(date_fed, time_format)
    date_cleaned = data.get("dateCleaned")
    if date_cleaned:
        date_cleaned = datetime.strptime(date_cleaned, time_format)
    date_weighed = data.get("dateWeighed")
    if date_weighed:
        date_weighed = datetime.strptime(date_weighed, time_format)
    date_shed = data.get("dateShed")
    if date_shed:
        date_shed = datetime.strptime(date_shed, time_format)
    date_eliminated = data.get("dateEliminated")
    if date_eliminated:
        date_eliminated = datetime.strptime(date_eliminated, time_format)

    pet = Pet(
        name=name,
        type=type,
        species=species,
        weight=weight,
        feed_frequency=feed_frequency,
        notes=notes,
        owner_id=owner_id,
        date_born=date_born,
        date_acquired=date_acquired,
        date_removed=date_removed,
        date_fed=date_fed,
        date_cleaned=date_cleaned,
        date_weighed=date_weighed,
        date_shed=date_shed,
        date_eliminated=date_eliminated,
    )
    db.session.add(pet)
    db.session.commit()
    return jsonify(one_pet_schema.dump(pet))
