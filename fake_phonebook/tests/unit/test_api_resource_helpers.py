import os
import sqlite3
from random import choice

from api.resources.helpers.list_people import get_people, get_person_by_id


def test_get_people():
    """
    api.resources.helpers.list_people.get_people() should return a list of names and a
    phone number.
    """

    list_of_people = get_people()
    assert str(type(list_of_people)) == "<class 'list'>"

    for i, person in enumerate(list_of_people):
        # For each person in the list, we'll assert that it should be represented by:
        """
        {
        ID: PERSON_ID,
        FULL_NAME: PERSON_FULL_NAME,
        PHONE_NUMBER: PERSON_PHONE_NUMBER
        }
        """
        # Remove the curly braces
        person_list = person[1 : len(person) - 1].split(",")
        assert len(person_list) == 3

        print(person_list[0])

        # Validate full_name
        full_name_field = person_list[1]
        full_name = full_name_field.split(":")[1].strip()
        assert full_name is not None

        # Validate phone numeber
        phone_number_field = person_list[2]
        phone_number = phone_number_field.split(":")[1].strip()
        assert phone_number.startswith("+")
        assert len(phone_number[1:].replace(" ", "")) == 12
        assert phone_number[1:].replace(" ", "").isnumeric()


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
    assert str(type(get_person_by_id(id))) == "<class 'str'>"
    assert get_person_by_id(id) is not None

    # For an id that doesn't exist, this should return None
    assert get_person_by_id("this-id-doesnt-exist") is None
