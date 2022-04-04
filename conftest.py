import pytest

from pet_helper import create_app, db
from pet_helper.models import User, Pet, Event

TEST_DATABASE_URI = "sqlite:///test_database.sqlite"


@pytest.fixture
def app():
    settings_override = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": TEST_DATABASE_URI,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SECRET_KEY": "dev",
    }

    app = create_app(settings_override)

    with app.app_context():
        db.init_app(app)
        from pet_helper.models import User, Event, Pet

        db.create_all()

        populate_test_data()

        yield app

        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


def populate_test_data():
    user_list = [
        User(username="Admin", role="admin"),
        User(username="SuperUser", role="super_user"),
        User(username="test_user"),
    ]
    for x in user_list:
        x.password = User.hash_password("test_password")
        db.session.add(x)
        db.session.commit()
