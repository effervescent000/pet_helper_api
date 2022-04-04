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
