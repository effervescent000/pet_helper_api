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
