from . import db
from passlib.hash import pbkdf2_sha256 as hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(200))

    pets = db.relationship(
        "Pet", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    events = db.relationship(
        "Event", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    @staticmethod
    def hash_password(password):
        return hash.hash(password)

    def check_password(self, input):
        return hash.verify(input, self.password)


class Pet(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(30), nullable=False)
    species = db.Column(db.String(50))
    weight = db.Column(db.Integer)
    feed_frequency = db.Column(db.Integer)
    is_alive = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

    date_born = db.Column(db.DateTime)
    date_acquired = db.Column(db.DateTime)
    date_removed = db.Column(db.DateTime)
    date_fed = db.Column(db.DateTime)
    date_cleaned = db.Column(db.DateTime)
    date_weighed = db.Column(db.DateTime)
    date_shed = db.Column(db.DateTime)
    date_eliminated = db.Column(db.DateTime)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    events = db.relationship(
        "Event", backref="pet", lazy=True, cascade="all, delete-orphan"
    )


class Event(db.Model):
    __tablename__ = "events"

    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    note = db.Column(db.Text)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"))
