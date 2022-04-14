import pytest
from datetime import datetime

from pet_helper.models import Pet
from pet_helper.utils import time_format as front_end_time_format

back_end_time_format = "%Y-%m-%dT%H:%M:%S"

# GET endpoint tests


def test_get_pets(client, admin_header, user_header):
    response = client.get("/pets/", headers=admin_header)
    assert response.status_code == 200
    data = response.json
    assert len(data) > 0

    response = client.get("/pets/", headers=user_header)
    assert response.status_code == 200

    response = client.get("/pets/")  # no headers
    assert response.status_code == 401


def test_get_pet_by_id_valid(client, user_header, admin_header):
    # accessing own pet returns the pet
    response = client.get("/pets/3", headers=user_header)
    assert response.status_code == 200
    data = response.json
    assert len(data) > 0

    # accessing someone else's pet as a regular user returns a 401
    response = client.get("/pets/1", headers=user_header)
    assert response.status_code == 401

    # accessing someone else's pet as an admin returns the pet
    response = client.get("/pets/3", headers=admin_header)
    assert response.status_code == 200
    data = response.json
    assert len(data) > 0


def test_get_pet_by_id_invalid(client, user_header):
    response = client.get("/pets/100000", headers=user_header)
    assert response.status_code == 400


# POST endpoint tests


@pytest.mark.parametrize(
    "input_data",
    [
        (
            {
                "name": "cupcake",
                "type": "snake",
                "species": "ball python",
                "weight": 1000,
                "feedFrequency": 20,
                "notes": "awww baby",
                "dateBorn": "2022-04-07T04:00:00.000Z",
                "dateRemoved": "",
            }
        )
    ],
)
def test_add_pet(client, user_header, input_data):
    response = client.post("/pets/", json=input_data)
    assert response.status_code == 401

    response = client.post("/pets/", json=input_data, headers=user_header)
    assert response.status_code == 200
    data = response.json
    assert data["id"]
    if input_data["name"]:
        assert input_data["name"] == data["name"]
    if input_data["dateBorn"]:
        assert datetime.strptime(
            input_data["dateBorn"], front_end_time_format
        ) == datetime.strptime(data["date_born"], back_end_time_format)


# PUT endpoint tests
@pytest.mark.parametrize("input_data,id", [({"name": "babypants", "dateBorn": ""}, 3)])
def test_update_pet_by_id(client, user_header, input_data, id):
    response = client.put(f"/pets/{id}", json=input_data)
    assert response.status_code == 401

    response = client.put(f"/pets/{id}", json=input_data, headers=user_header)
    assert response.status_code == 200
    data = response.json
    if input_data["name"]:
        assert input_data["name"] == data["name"]
    if input_data["dateBorn"]:
        assert input_data["dateBorn"] == data["date_born"]
