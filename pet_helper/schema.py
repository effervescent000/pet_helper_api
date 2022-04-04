from . import ma


class EventSchema(ma.Schema):
    class Meta:
        fields = ("id", "date", "type", "note", "owner_id", "pet_id")


multi_event_schema = EventSchema(many=True)


class PetSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "name",
            "type",
            "species",
            "weight",
            "feed_frequency",
            "is_alive",
            "notes",
            "date_born",
            "date_acquired",
            "date_removed",
            "date_fed",
            "date_cleaned",
            "date_weighed",
            "date_shed",
            "date_eliminated",
            "owner_id",
            "events",
        )

    events = ma.Nested(multi_event_schema)


multi_pet_schema = PetSchema(many=True)


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "role", "events", "pets")

    events = ma.Nested(multi_event_schema)
    pets = ma.Nested(multi_pet_schema)
