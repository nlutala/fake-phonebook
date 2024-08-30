from random import choice
from unittest.mock import Mock

import pytest
from api.resources.http_methods.delete import (
    delete_contact_from_db,
    delete_contacts_from_db,
)
from api.resources.http_methods.get import get_contact_by_id, get_contacts
from api.resources.http_methods.post import post_contact_to_db


def test_delete_contacts_from_db():
    """
    api.resources.http_methods.delete.delete_contacts_from_db() should return a list of
    dictionaries consisting the id, name and phone_number of the contacts deleted
    from the database as key-value pairs or None if the contacts could not be deleted
    from the database successfully.
    """
    # 1. Add 3 contacts to the db
    contact_1 = {"name": "contact One", "phone_number": "+44 7123452617"}
    contact_1_id = post_contact_to_db(contact_1)

    contact_2 = {"name": "contact Two", "phone_number": "+44 7122452617"}
    contact_2_id = post_contact_to_db(contact_2)

    contact_3 = {"name": "contact Three", "phone_number": "+44 7123432617"}
    contact_3_id = post_contact_to_db(contact_3)

    # 2. Assert that no one is deleted if none of the dictionaries has an "id" key-value
    # pair
    contacts_before = get_contacts()

    delete_contacts_from_db(
        [
            {"not-an-id-1": contact_1_id},
            {"not-an-id-2": contact_2_id},
            {"not-an-id-3": contact_3_id},
        ]
    )

    contacts_after = get_contacts()

    assert len(contacts_before) == len(contacts_after)
    assert get_contact_by_id(contact_1_id) == {
        "id": contact_1_id,
        "name": contact_1.get("name"),
        "phone_number": contact_1.get("phone_number"),
    }
    assert get_contact_by_id(contact_2_id) == {
        "id": contact_2_id,
        "name": contact_2.get("name"),
        "phone_number": contact_2.get("phone_number"),
    }
    assert get_contact_by_id(contact_3_id) == {
        "id": contact_3_id,
        "name": contact_3.get("name"),
        "phone_number": contact_3.get("phone_number"),
    }

    # 3. Assert that 2 of the three contacts are deleted from the database if only two of
    # the dictionaries have an "id" key-value pair
    delete_contacts_from_db(
        [
            {"id": contact_1_id},
            {"id": contact_2_id},
            {"not-an-id-3": contact_3_id},
        ]
    )

    contacts_after = get_contacts()

    # contact_1 and contact_2 should have been deleted from the database
    assert len(contacts_before) == len(contacts_after) + 2
    assert get_contact_by_id(contact_1_id) is None
    assert get_contact_by_id(contact_2_id) is None
    assert get_contact_by_id(contact_3_id) == {
        "id": contact_3_id,
        "name": contact_3.get("name"),
        "phone_number": contact_3.get("phone_number"),
    }

    # 4. Assert that only contact_3 should be deleted from the database as contact_1 and
    # contact_2 were already deleted.
    delete_contacts_from_db(
        [
            {"id": contact_1_id},
            {"id": contact_2_id},
            {"id": contact_3_id},
        ]
    )

    contacts_after = get_contacts()

    # contact_1 and contact_2 should have been deleted from the database
    assert len(contacts_before) == len(contacts_after) + 3
    assert get_contact_by_id(contact_1_id) is None
    assert get_contact_by_id(contact_2_id) is None
    assert get_contact_by_id(contact_3_id) is None


def test_delete_contact_from_db():
    """
    api.resources.http_methods.delete.delete_contact_from_db() should return a
    dictionary consisting the id, name and phone_number of the contact deleted
    from the database as key-value pairs or None if the contacts could not be deleted
    from the database successfully.
    """
    contacts_before = get_contacts()
    contact = choice(contacts_before)
    contact_id = contact.get("id")
    contact_incorrect_id = contact_id + "-incorrect"
    contact["id"] = contact_incorrect_id

    # Step 1. Assert that the contact was not deleted if the id of the contact is not
    # correct.
    delete_contact_from_db(contact) is None
    assert len(get_contacts()) == len(contacts_before)

    # Step 2. Assert that the contact is deleted from the db if the correct id is
    # in the dictionary passed through as a parameter
    contact["id"] = contact_id

    delete_contact_from_db(contact) == contact
    assert len(get_contacts()) == len(contacts_before) - 1

    # Add contact back to the db (they'll have a new id but it's fine)
    post_contact_to_db(
        {
            "name": contact.get("name"),
            "phone_number": contact.get("phone_number"),
        }
    )

    assert len(get_contacts()) == len(contacts_before)
