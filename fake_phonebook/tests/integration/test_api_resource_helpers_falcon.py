import os
import sqlite3
from random import choice
from unittest.mock import Mock

from api.resources.helpers.list_people import (
    add_people_to_db,
    delete_people_from_db,
    delete_person_from_db,
    get_people,
    get_person_by_id,
    post_person_to_db,
)
from faker import Faker
from pytest_mock import mocker


def test_delete_people_from_db(mocker: Mock):
    """
    api.resources.helpers.list_people.delete_people_from_db() should return a list of
    dictionaries consisting the id, full_name and phone_number of the people deleted
    from the database as key-value pairs or None if the people could not be deleted
    from the database successfully.
    """
    pass  # Needs to be an integration test (will do with falcon)
