from datetime import date
import pytest
from flask_jwt_extended import create_access_token

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
        "JWT_HEADER_TYPE": "Bearer",
        "JWT_BLACKLIST_ENABLED": False,
        "JWT_TOKEN_LOCATION": ["headers"],
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
def admin_header():
    return {
        "Authorization": f"Bearer {create_access_token(identity=User.query.filter_by(username='Admin').first())}"
    }


@pytest.fixture
def user_header():
    return {
        "Authorization": f"Bearer {create_access_token(identity=User.query.filter_by(username='test_user').first())}"
    }


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

    pet_list = [
        Pet(
            name="Rainbow Sherbert",
            type="snake",
            species="corn snake",
            weight=500,
            feed_frequency=10,
            notes="cutie patootie",
            date_fed=date.today(),
            date_cleaned=date.today(),
            owner_id=1,
        ),
        Pet(
            name="Sweetheart",
            type="snake",
            species="ball python",
            weight=800,
            feed_frequency=18,
            date_shed=date.today(),
            owner_id=1,
        ),
    ]
    for x in pet_list:
        db.session.add(x)
        db.session.commit()

    events_list = [
        Event(
            date=date.today(),
            type="feed reject",
            note="test event here is an item",
            owner_id=1,
            pet_id=2,
        ),
        Event(
            date=date.today(),
            type="feed success",
            owner_id=1,
            pet_id=1,
        ),
    ]
    for x in events_list:
        db.session.add(x)
        db.session.commit()
