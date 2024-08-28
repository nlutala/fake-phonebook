from random import choice
from unittest.mock import Mock

import pytest
from api.resources.http_methods.delete import (
    delete_people_from_db,
    delete_person_from_db,
)
from api.resources.http_methods.get import get_people, get_person_by_id
from api.resources.http_methods.post import post_person_to_db


def test_delete_people_from_db():
    """
    api.resources.http_methods.delete.delete_people_from_db() should return a list of
    dictionaries consisting the id, full_name and phone_number of the people deleted
    from the database as key-value pairs or None if the people could not be deleted
    from the database successfully.
    """
    # 1. Add 3 people to the db
    person_1 = {"full_name": "Person One", "phone_number": "+44 7123452617"}
    person_1_id = post_person_to_db(person_1)

    person_2 = {"full_name": "Person Two", "phone_number": "+44 7122452617"}
    person_2_id = post_person_to_db(person_2)

    person_3 = {"full_name": "Person Three", "phone_number": "+44 7123432617"}
    person_3_id = post_person_to_db(person_3)

    # 2. Assert that no one is deleted if none of the dictionaries has an "id" key-value
    # pair
    people_before = get_people()

    delete_people_from_db(
        [
            {"not-an-id-1": person_1_id},
            {"not-an-id-2": person_2_id},
            {"not-an-id-3": person_3_id},
        ]
    )

    people_after = get_people()

    assert len(people_before) == len(people_after)
    assert get_person_by_id(person_1_id) == {
        "id": person_1_id,
        "full_name": person_1.get("full_name"),
        "phone_number": person_1.get("phone_number"),
    }
    assert get_person_by_id(person_2_id) == {
        "id": person_2_id,
        "full_name": person_2.get("full_name"),
        "phone_number": person_2.get("phone_number"),
    }
    assert get_person_by_id(person_3_id) == {
        "id": person_3_id,
        "full_name": person_3.get("full_name"),
        "phone_number": person_3.get("phone_number"),
    }

    # 3. Assert that 2 of the three people are deleted from the database if only two of
    # the dictionaries have an "id" key-value pair
    delete_people_from_db(
        [
            {"id": person_1_id},
            {"id": person_2_id},
            {"not-an-id-3": person_3_id},
        ]
    )

    people_after = get_people()

    # person_1 and person_2 should have been deleted from the database
    assert len(people_before) == len(people_after) + 2
    assert get_person_by_id(person_1_id) is None
    assert get_person_by_id(person_2_id) is None
    assert get_person_by_id(person_3_id) == {
        "id": person_3_id,
        "full_name": person_3.get("full_name"),
        "phone_number": person_3.get("phone_number"),
    }

    # 4. Assert that only person_3 should be deleted from the database as person_1 and
    # person_2 were already deleted.
    delete_people_from_db(
        [
            {"id": person_1_id},
            {"id": person_2_id},
            {"id": person_3_id},
        ]
    )

    people_after = get_people()

    # person_1 and person_2 should have been deleted from the database
    assert len(people_before) == len(people_after) + 3
    assert get_person_by_id(person_1_id) is None
    assert get_person_by_id(person_2_id) is None
    assert get_person_by_id(person_3_id) is None


def test_delete_person_from_db():
    """
    api.resources.http_methods.delete.delete_person_from_db() should return a
    dictionary consisting the id, full_name and phone_number of the person deleted
    from the database as key-value pairs or None if the people could not be deleted
    from the database successfully.
    """
    people_before = get_people()
    person = choice(people_before)
    person_id = person.get("id")
    person_incorrect_id = person_id + "-incorrect"
    person["id"] = person_incorrect_id

    # Step 1. Assert that the person was not deleted if the id of the person is not
    # correct.
    delete_person_from_db(person) is None
    assert len(get_people()) == len(people_before)

    # Step 2. Assert that the person is deleted from the db if the correct id is
    # in the dictionary passed through as a parameter
    person["id"] = person_id

    delete_person_from_db(person) == person
    assert len(get_people()) == len(people_before) - 1

    # Add person back to the db (they'll have a new id but it's fine)
    post_person_to_db(
        {
            "full_name": person.get("full_name"),
            "phone_number": person.get("phone_number"),
        }
    )

    assert len(get_people()) == len(people_before)
