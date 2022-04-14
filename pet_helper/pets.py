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

    date_born = (
        datetime.strptime(data.get("dateBorn"), time_format)
        if data.get("dateBorn")
        else None
    )
    date_acquired = (
        datetime.strptime(data.get("dateAcquired"), time_format)
        if data.get("dateAcquired")
        else None
    )
    date_removed = (
        datetime.strptime(data.get("dateRemoved"), time_format)
        if data.get("dateRemoved")
        else None
    )
    date_fed = (
        datetime.strptime(data.get("dateFed"), time_format)
        if data.get("dateFed")
        else None
    )
    date_cleaned = (
        datetime.strptime(data.get("dateCleaned"), time_format)
        if data.get("dateCleaned")
        else None
    )
    date_weighed = (
        datetime.strptime(data.get("dateWeighed"), time_format)
        if data.get("dateWeighed")
        else None
    )
    date_shed = (
        datetime.strptime(data.get("dateShed"), time_format)
        if data.get("dateShed")
        else None
    )
    date_eliminated = (
        datetime.strptime(data.get("dateEliminated"), time_format)
        if data.get("dateEliminated")
        else None
    )

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


# PUT endpoints
@bp.route("/<id>", methods=["PUT"])
@jwt_required()
def update_pet_by_id(id):
    data = request.get_json()
    pet = Pet.query.get(id)
    if pet.owner_id == current_user.id:
        name = data.get("name")
        type = data.get("type")
        species = data.get("species")
        weight = data.get("weight")
        feed_frequency = data.get("feedFrequency")
        notes = data.get("notes")

        date_born = data.get("dateBorn")
        date_acquired = data.get("dateAcquired")
        date_removed = data.get("dateRemoved")
        date_fed = data.get("dateFed")
        date_cleaned = data.get("dateCleaned")
        date_weighed = data.get("dateWeighed")
        date_shed = data.get("dateShed")
        date_eliminated = data.get("dateEliminated")

        pet.name = name if name else pet.name
        pet.type = type if type else pet.type
        pet.species = species if species else pet.species
        pet.weight = weight if weight else pet.weight
        pet.feed_frequency = feed_frequency if feed_frequency else pet.feed_frequency
        pet.notes = notes if notes else pet.notes

        pet.date_born = (
            datetime.strptime(date_born, time_format) if date_born else pet.date_born
        )
        pet.date_acquired = (
            datetime.strptime(date_acquired, time_format)
            if date_acquired
            else pet.date_acquired
        )
        pet.date_removed = (
            datetime.strptime(date_removed, time_format)
            if date_removed
            else pet.date_removed
        )
        pet.date_fed = (
            datetime.strptime(date_fed, time_format) if date_fed else pet.date_fed
        )
        pet.date_cleaned = (
            datetime.strptime(date_cleaned, time_format)
            if date_cleaned
            else pet.date_cleaned
        )
        pet.date_weighed = (
            datetime.strptime(date_weighed, time_format)
            if date_weighed
            else pet.date_weighed
        )
        pet.date_shed = (
            datetime.strptime(date_shed, time_format) if date_shed else pet.date_shed
        )
        pet.date_eliminated = (
            datetime.strptime(date_eliminated, time_format)
            if date_eliminated
            else pet.date_eliminated
        )

        db.session.commit()
        return jsonify(one_pet_schema.dump(pet))

    return jsonify({"error": "unauthorized"}), 401
