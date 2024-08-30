import os
import sqlite3
from random import choice
from string import ascii_lowercase
from unittest.mock import Mock

from api.resources.helpers.env import PATH_TO_DB
from api.resources.http_methods.delete import delete_contact_from_db
from api.resources.http_methods.get import (
    get_contact_by_id,
    get_contacts,
    get_contacts_starting_with,
)
from api.resources.http_methods.post import add_contacts_to_db, post_contact_to_db
from api.resources.http_methods.update import update_contact_in_db
from faker import Faker
from pytest_mock import mocker


# ========================= Tests for POST methods (Create) ==========================
def test_add_contacts_to_db():
    """
    api.resources.helpers.list_contacts.add_contacts_to_db() should return how many contacts
    were inserted into the db.

    It should not allow for inserting a contact into the database if a record with the
    same name already exists in the db
    """
    contact1_name = Faker().name()
    contact2_name = Faker().name()

    contacts = [
        (
            f"test-add-contacts-to-db-{choice([range(10000)])}",
            contact1_name,
            "+44 1234567891",
        ),  # Doesn't exist in the db... yet
        (
            f"test-add-contacts-to-db-{choice(range(10000))}",
            contact2_name,
            "+44 1234567891",
        ),  # Doesn't exist in the db... yet
    ]

    # Use case 1: Assert that after inserting someone into the db, add_contacts_to_db
    # returns 1
    assert add_contacts_to_db([contacts[0]]) == 1

    # Use case 2: Assert that after trying to insert someone (that is already in the db)
    # into the db, add_contacts_to_db returns 0
    assert add_contacts_to_db([contacts[0]]) == 0

    # Use case 3: Assert that after trying to insert someone (that is already in the db)
    # into the db, and someone that is not into the db, add_contacts_to_db returns 1
    assert add_contacts_to_db(contacts) == 1

    # Remove side-effects from the test
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    cur.execute(
        f"delete from contacts where id in ('{contacts[0][0]}', '{contacts[1][0]}')"
    )
    con.commit()
    con.close()


def test_post_contact_to_db(mocker: Mock):
    """
    api.resources.helpers.list_contacts.post_contact_to_db() should return the id of the
    new contact added to the database or None if the contact is already in the db.
    """
    name = f"Test {Faker().name()}"
    phone_number = "+44 1234567891"

    first_name = name.split(" ")[0]
    last_name = " ".join(name.split(" ")[1:])

    # We want to enfore that the json (well, now dictionary) representing the contact
    # Should have a name and phone_number key, value pairs.
    contact = {"email_address": f"{first_name}.{last_name}@example.com".lower()}
    assert post_contact_to_db(contact) is None

    # After adding the name to the contact, post_contact_to_db should be None
    contact["name"] = name
    assert post_contact_to_db(contact) is None

    mocker.patch(
        "api.resources.http_methods.post.add_contacts_to_db",
        return_value=1,
    )

    # Now that we have added the phone number (and that this contact doesn't exist in the
    # db), post_contact_to_db should return a string id for this contact.
    contact["phone_number"] = phone_number

    contact_id = post_contact_to_db(contact)
    assert contact_id is not None
    assert str(type(contact_id)) == "<class 'str'>"

    # Now if we try to post this contact again, post_contact_to_db should return None,
    # because they now exist in the db
    mocker.patch(
        "api.resources.http_methods.post.add_contacts_to_db",
        return_value=0,
    )

    contact_id = post_contact_to_db(contact)
    assert contact_id is None

    # Remove side-effects from the test
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    cur.execute(f"delete from contacts where phone_number = '{phone_number}'")
    con.commit()
    con.close()


# =========================== Tests for GET methods (Read) ============================
def test_get_contacts():
    """
    api.resources.helpers.list_contacts.get_contacts() should return a list of dictionaries
    to represent contacts as id, name and phone_number.
    """
    list_of_contacts = get_contacts()
    assert str(type(list_of_contacts)) == "<class 'list'>"

    for contact in list_of_contacts:
        assert len(contact.keys()) == 3

        # Validate that each contact has an id
        assert contact.get("id") is not None
        assert str(type(contact.get("id"))) == "<class 'str'>"

        # Validate name
        assert contact.get("name") is not None
        assert str(type(contact.get("name"))) == "<class 'str'>"

        # Validate phone numeber
        assert contact.get("phone_number") is not None
        assert str(type(contact.get("phone_number"))) == "<class 'str'>"
        assert contact.get("phone_number").startswith("+")
        assert len(contact.get("phone_number")[1:].replace(" ", "")) == 12
        assert contact.get("phone_number")[1:].replace(" ", "").isnumeric()


def test_get_contact_by_id():
    """
    api.resources.helpers.list_contacts.get_contact_by_id() should return a dictionary
    to represent a contact as id, name and phone_number.

    If the contact doesn't exist. Return null.
    """
    # Get a list of valid ids of contacts in the database
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    ids = [id[0] for id in cur.execute("SELECT id FROM contacts")]
    con.close()

    # Randomly choose one of these ids to test the get_contact_by_id with
    # The response of the get_contact_by_id() function should not be None
    id = choice(ids)
    assert str(type(get_contact_by_id(id))) == "<class 'dict'>"
    assert get_contact_by_id(id) is not None

    # For an id that doesn't exist, this should return None
    assert get_contact_by_id("this-id-doesnt-exist") is None


def test_get_contacts_starting_with():
    """
    api.resources.helpers.list_contacts.get_contacts_starting_with() should return a list
    of contacts represented as a dictionary with id, name and phone_number key-value
    pairs.

    Return None if:
    - There isn't anyone who's name starts with a the letter or string.
    - The user of the api doesn't add a string that is at least 1 character long
    """
    # Assert that an empty string should return None
    assert get_contacts_starting_with("") is None
    assert get_contacts_starting_with("      ") is None

    # Assert that get_contacts_starting_with("no-one-has-this-name") should return None
    assert get_contacts_starting_with("no-one-has-this-name") is None

    # Assert that get_contacts_starting_with(letter) returns contacts whose full name starts
    # with a letter
    for contact in get_contacts_starting_with("d"):
        assert contact.get("name").lower().startswith("d")


# =========================== Tests for PUT methods (Update) ===========================
def test_update_contact_in_db(mocker: Mock):
    """
    api.resources.helpers.list_contacts.update_contact_in_db() should return the id,
    (new) name and/or (new) phone_number of the contact added to the database or
    None if the contact could not be deleted from the database successfully.
    """
    # Get a random contact from the database
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    contacts = [
        record for record in cur.execute("SELECT id, name, phone_number FROM contacts")
    ]
    con.close()
    original_contact = choice(contacts)

    # If the user of the api does not send an id key-value pair, update_contact_in_db()
    # should return None
    contact = {"email_address": "another.fake.email@example.com"}
    assert update_contact_in_db(contact) is None

    # If the user of the api sends an id key-value pair, but the id does not exist in
    # the database, update_contact_in_db() should return None
    mocker.patch(
        "api.resources.http_methods.get.get_contact_by_id",
        return_value=None,
    )
    contact["id"] = "this-id-doesnt-exist"
    assert update_contact_in_db(contact) is None

    # If the user of the api sends an id key-value pair, and the id does exist in
    # the database, but they have not added key-value pairs for a name or phone
    # number, update_contact_in_db() should return None
    mocker.patch(
        "api.resources.http_methods.get.get_contact_by_id",
        return_value={
            "id": original_contact[0],
            "name": original_contact[1],
            "phone_number": original_contact[2],
        },
    )
    contact["id"] = original_contact[0]
    assert update_contact_in_db(contact) is None

    # If the user of the api sends an id key-value pair, and the id does exist in
    # the database, they have added a key-value pair for a name but not a phone
    # number, update_contact_in_db() should return a dictionary with the contact's id,
    # updated name and original phone number
    mocker.patch(
        "api.resources.http_methods.get.get_contact_by_id",
        return_value={
            "id": original_contact[0],
            "name": "Test contact",
            "phone_number": original_contact[2],
        },
    )
    contact["name"] = "Test contact"
    assert update_contact_in_db(contact) == {
        "id": original_contact[0],
        "name": "Test contact",
        "phone_number": original_contact[2],
    }

    # If the user of the api sends an id key-value pair, and the id does exist in
    # the database, they have not added a key-value pair for a name but they have
    # for a phone number, update_contact_in_db() should return a dictionary with the
    # contact's id, original name and updated phone number
    mocker.patch(
        "api.resources.http_methods.get.get_contact_by_id",
        return_value={
            "id": original_contact[0],
            "name": original_contact[1],
            "phone_number": "+44 1234567890",
        },
    )
    contact["phone_number"] = "+44 1234567890"
    contact["name"] = original_contact[1]
    assert update_contact_in_db(contact) == {
        "id": original_contact[0],
        "name": original_contact[1],
        "phone_number": "+44 1234567890",
    }

    # If the user of the api sends an id key-value pair, and the id does exist in
    # the database, they have added a key-value pair for a name and phone number,
    # update_contact_in_db() should return a dictionary with the contact's id,
    # updated name and updated phone number
    contact["name"] = "Test contact"
    contact["phone_number"] = "+44 1234567890"

    mocker.patch(
        "api.resources.http_methods.get.get_contact_by_id",
        return_value={
            "id": original_contact[0],
            "name": "Test contact",
            "phone_number": "+44 1234567890",
        },
    )
    assert update_contact_in_db(contact) == {
        "id": original_contact[0],
        "name": "Test contact",
        "phone_number": "+44 1234567890",
    }

    # Undo side effects
    delete_contact_from_db({"id": original_contact[0]})
    post_contact_to_db(
        {"name": original_contact[1], "phone_number": original_contact[2]}
    )


# ========================= Tests for DELETE method (Delete) ==========================
def test_delete_contact_from_db(mocker: Mock):
    """
    api.resources.helpers.list_contacts.delete_contact_from_db() should return the id,
    name and phone_number of the contact added to the database or None if the contact
    could not be deleted from the database successfully.
    """
    # Get a list of valid ids of contacts in the database
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    contacts = [
        record for record in cur.execute("SELECT id, name, phone_number FROM contacts")
    ]
    con.close()

    # Randomly choose one of these contacts to test the delete_contact_from_db with
    contact = choice(contacts)

    # Instantiate a new variable p (which we will use from now on for testing)
    # Give p a fake email (this doesn't matter), but we want to assert that if
    # we give the delete_contact_from_db() function a dictionary without an id key-value
    # pair, we should get None.
    p = {"email_address": "fake.email@example.com"}
    assert delete_contact_from_db(p) is None

    # Now let's update p to have the id key-value pair. But this id does not exist in
    # the database
    mocker.patch(
        "api.resources.http_methods.get.get_contact_by_id",
        return_value=None,
    )
    p["id"] = "a-contact-with-this-id-does-not-exist"
    assert delete_contact_from_db(p) is None

    # Now let's update p to have the id key-value pair, with this id existing in
    # the database
    mocker.patch(
        "api.resources.http_methods.get.get_contact_by_id",
        return_value={
            "id": contact[0],
            "name": contact[1],
            "phone_number": contact[2],
        },
    )
    p["id"] = contact[0]
    assert delete_contact_from_db(p) == {
        "id": contact[0],
        "name": contact[1],
        "phone_number": contact[2],
    }

    # Validate that this contact no longer exists in the database
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    contacts = [
        record
        for record in cur.execute(f"SELECT * FROM contacts WHERE id = '{p.get('id')}'")
    ]
    con.close()

    assert len(contacts) == 0

    # Add this contact back into the database as this was only a test (undo side effects)
    post_contact_to_db(p)
