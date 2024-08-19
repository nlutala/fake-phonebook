import os
import sqlite3
from random import choice

from api.resources.helpers.list_people import get_people, get_person_by_id


def test_get_people():
    """
    api.resources.helpers.list_people.get_people() should return a list of dictionaries
    to represent people as id, full_name and phone_number.
    """

    list_of_people = get_people()
    assert str(type(list_of_people)) == "<class 'list'>"

    for person in list_of_people:
        assert len(person.keys()) == 3

        # Validate that eacg person has an id
        assert person.get("id") is not None
        assert str(type(person.get("id"))) == "<class 'str'>"

        # Validate full_name
        assert person.get("full_name") is not None
        assert str(type(person.get("full_name"))) == "<class 'str'>"

        # Validate phone numeber
        assert person.get("phone_number") is not None
        assert str(type(person.get("phone_number"))) == "<class 'str'>"
        assert person.get("phone_number").startswith("+")
        assert len(person.get("phone_number")[1:].replace(" ", "")) == 12
        assert person.get("phone_number")[1:].replace(" ", "").isnumeric()


def test_get_person_by_id():
    # Get a list of valid ids of people in the database
    parent_dir = os.path.dirname(__file__).partition("tests")[0]
    path_to_db = os.path.join(parent_dir, "fake_people.db")
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    ids = [id[0] for id in cur.execute("SELECT id FROM people")]
    con.close()

    # Randomly choose one of these ids to test the get_person_by_id with
    # The response of the get_person_by_id() function should not be None
    id = choice(ids)
    assert str(type(get_person_by_id(id))) == "<class 'dict'>"
    assert get_person_by_id(id) is not None

    # For an id that doesn't exist, this should return None
    assert get_person_by_id("this-id-doesnt-exist") is None
