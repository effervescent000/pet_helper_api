import pytest

from pet_helper.models import Pet

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
                "feed_frequency": 20,
                "notes": "awww baby",
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
    for item in input_data.keys():
        assert input_data[item] == data[item]
