import os
import sqlite3
from random import choice
from string import ascii_lowercase
from unittest.mock import Mock

from api.resources.helpers.env import PATH_TO_DB
from api.resources.http_methods.delete import delete_person_from_db
from api.resources.http_methods.get import (
    get_people,
    get_people_starting_with,
    get_person_by_id,
)
from api.resources.http_methods.post import add_people_to_db, post_person_to_db
from api.resources.http_methods.update import update_person_in_db
from faker import Faker
from pytest_mock import mocker


# ========================= Tests for POST methods (Create) ==========================
def test_add_people_to_db():
    """
    api.resources.helpers.list_people.add_people_to_db() should return how many people
    were inserted into the db.

    It should not allow for inserting a person into the database if a record with the
    same full_name already exists in the db
    """
    person1_name = Faker().name()
    person2_name = Faker().name()

    people = [
        (
            f"test-add-people-to-db-{choice([range(10000)])}",
            person1_name,
            person1_name.split(" ")[0],
            person1_name.split(" ")[1],
            f"""{
                person1_name.split(" ")[0]
            }.{
                person1_name.split(" ")[1]
            }@example.com""".lower(),
            "+44 1234567891",
            f"""www.linkedin.com/{
                person1_name.split(" ")[0]
            }-{
                person1_name.split(" ")[1]
            }""".lower(),
        ),  # Doesn't exist in the db... yet
        (
            f"test-add-people-to-db-{choice(range(10000))}",
            person2_name,
            person2_name.split(" ")[0],
            person2_name.split(" ")[1],
            f"""{
                person2_name.split(" ")[0]
            }.{
                person2_name.split(" ")[1]
            }@example.com""".lower(),
            "+44 1234567891",
            f"""www.linkedin.com/{
                person2_name.split(" ")[0]
            }-{
                person2_name.split(" ")[1]
            }""".lower(),
        ),  # Doesn't exist in the db... yet
    ]

    # Use case 1: Assert that after inserting someone into the db, add_people_to_db
    # returns 1
    assert add_people_to_db([people[0]]) == 1

    # Use case 2: Assert that after trying to insert someone (that is already in the db)
    # into the db, add_people_to_db returns 0
    assert add_people_to_db([people[0]]) == 0

    # Use case 3: Assert that after trying to insert someone (that is already in the db)
    # into the db, and someone that is not into the db, add_people_to_db returns 1
    assert add_people_to_db(people) == 1

    # Remove side-effects from the test
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    cur.execute(f"delete from people where id in ('{people[0][0]}', '{people[1][0]}')")
    con.commit()
    con.close()


def test_post_person_to_db(mocker: Mock):
    """
    api.resources.helpers.list_people.post_person_to_db() should return the id of the
    new person added to the database or None if the person is already in the db.
    """
    full_name = f"Test {Faker().name()}"
    first_name = full_name.split(" ")[0]
    last_name = " ".join(full_name.split(" ")[1:])
    phone_number = "+44 1234567891"

    # We want to enfore that the json (well, now dictionary) representing the person
    # Should have a full_name and phone_number key, value pairs.
    person = {"email_address": f"{first_name}.{last_name}@example.com".lower()}
    assert post_person_to_db(person) is None

    # After adding the full_name to the person, post_person_to_db should be None
    person["full_name"] = full_name
    assert post_person_to_db(person) is None

    mocker.patch(
        "api.resources.http_methods.post.add_people_to_db",
        return_value=1,
    )

    # Now that we have added the phone number (and that this person doesn't exist in the
    # db), post_person_to_db should return a string id for this person.
    person["phone_number"] = phone_number

    person_id = post_person_to_db(person)
    assert person_id is not None
    assert str(type(person_id)) == "<class 'str'>"

    # Now if we try to post this person again, post_person_to_db should return None,
    # because they now exist in the db
    mocker.patch(
        "api.resources.http_methods.post.add_people_to_db",
        return_value=0,
    )

    person_id = post_person_to_db(person)
    assert person_id is None

    # Remove side-effects from the test
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    cur.execute(f"delete from people where phone_number = '{phone_number}'")
    con.commit()
    con.close()


# =========================== Tests for GET methods (Read) ============================
def test_get_people():
    """
    api.resources.helpers.list_people.get_people() should return a list of dictionaries
    to represent people as id, full_name and phone_number.
    """
    list_of_people = get_people()
    assert str(type(list_of_people)) == "<class 'list'>"

    for person in list_of_people:
        assert len(person.keys()) == 3

        # Validate that each person has an id
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
    """
    api.resources.helpers.list_people.get_person_by_id() should return a dictionary
    to represent a person as id, full_name and phone_number.

    If the person doesn't exist. Return null.
    """
    # Get a list of valid ids of people in the database
    con = sqlite3.connect(PATH_TO_DB)
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


def test_get_people_starting_with():
    """
    api.resources.helpers.list_people.get_people_starting_with() should return a list
    of people represented as a dictionary with id, full_name and phone_number key-value
    pairs.

    Return None if:
    - There isn't anyone who's name starts with a the letter or string.
    - The user of the api doesn't add a string that is at least 1 character long
    """
    # Assert that an empty string should return None
    assert get_people_starting_with("") is None
    assert get_people_starting_with("      ") is None

    # Assert that get_people_starting_with("no-one-has-this-name") should return None
    assert get_people_starting_with("no-one-has-this-name") is None

    # Assert that get_people_starting_with(letter) returns people whose full name starts
    # with a letter
    for person in get_people_starting_with("d"):
        assert person.get("full_name").lower().startswith("d")


# =========================== Tests for PUT methods (Update) ===========================
def test_update_person_in_db(mocker: Mock):
    """
    api.resources.helpers.list_people.update_person_in_db() should return the id,
    (new) full_name and/or (new) phone_number of the person added to the database or
    None if the person could not be deleted from the database successfully.
    """
    # Get a random person from the database
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    people = [
        record
        for record in cur.execute("SELECT id, full_name, phone_number FROM people")
    ]
    con.close()
    original_person = choice(people)

    # If the user of the api does not send an id key-value pair, update_person_in_db()
    # should return None
    person = {"email_address": "another.fake.email@example.com"}
    assert update_person_in_db(person) is None

    # If the user of the api sends an id key-value pair, but the id does not exist in
    # the database, update_person_in_db() should return None
    mocker.patch(
        "api.resources.http_methods.get.get_person_by_id",
        return_value=None,
    )
    person["id"] = "this-id-doesnt-exist"
    assert update_person_in_db(person) is None

    # If the user of the api sends an id key-value pair, and the id does exist in
    # the database, but they have not added key-value pairs for a full_name or phone
    # number, update_person_in_db() should return None
    mocker.patch(
        "api.resources.http_methods.get.get_person_by_id",
        return_value={
            "id": original_person[0],
            "full_name": original_person[1],
            "phone_number": original_person[2],
        },
    )
    person["id"] = original_person[0]
    assert update_person_in_db(person) is None

    # If the user of the api sends an id key-value pair, and the id does exist in
    # the database, they have added a key-value pair for a full_name but not a phone
    # number, update_person_in_db() should return a dictionary with the person's id,
    # updated full_name and original phone number
    mocker.patch(
        "api.resources.http_methods.get.get_person_by_id",
        return_value={
            "id": original_person[0],
            "full_name": "Test Person",
            "phone_number": original_person[2],
        },
    )
    person["full_name"] = "Test Person"
    assert update_person_in_db(person) == {
        "id": original_person[0],
        "full_name": "Test Person",
        "phone_number": original_person[2],
    }

    # If the user of the api sends an id key-value pair, and the id does exist in
    # the database, they have not added a key-value pair for a full_name but they have
    # for a phone number, update_person_in_db() should return a dictionary with the
    # person's id, original full_name and updated phone number
    mocker.patch(
        "api.resources.http_methods.get.get_person_by_id",
        return_value={
            "id": original_person[0],
            "full_name": original_person[1],
            "phone_number": "+44 1234567890",
        },
    )
    person["phone_number"] = "+44 1234567890"
    person["full_name"] = original_person[1]
    assert update_person_in_db(person) == {
        "id": original_person[0],
        "full_name": original_person[1],
        "phone_number": "+44 1234567890",
    }

    # If the user of the api sends an id key-value pair, and the id does exist in
    # the database, they have added a key-value pair for a full_name and phone number,
    # update_person_in_db() should return a dictionary with the person's id,
    # updated full_name and updated phone number
    person["full_name"] = "Test Person"
    person["phone_number"] = "+44 1234567890"

    mocker.patch(
        "api.resources.http_methods.get.get_person_by_id",
        return_value={
            "id": original_person[0],
            "full_name": "Test Person",
            "phone_number": "+44 1234567890",
        },
    )
    assert update_person_in_db(person) == {
        "id": original_person[0],
        "full_name": "Test Person",
        "phone_number": "+44 1234567890",
    }

    # Undo side effects
    delete_person_from_db({"id": original_person[0]})
    post_person_to_db(
        {"full_name": original_person[1], "phone_number": original_person[2]}
    )


# ========================= Tests for DELETE method (Delete) ==========================
def test_delete_person_from_db(mocker: Mock):
    """
    api.resources.helpers.list_people.delete_person_from_db() should return the id,
    full_name and phone_number of the person added to the database or None if the person
    could not be deleted from the database successfully.
    """
    # Get a list of valid ids of people in the database
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    people = [
        record
        for record in cur.execute("SELECT id, full_name, phone_number FROM people")
    ]
    con.close()

    # Randomly choose one of these people to test the delete_person_from_db with
    person = choice(people)

    # Instantiate a new variable p (which we will use from now on for testing)
    # Give p a fake email (this doesn't matter), but we want to assert that if
    # we give the delete_person_from_db() function a dictionary without an id key-value
    # pair, we should get None.
    p = {"email_address": "fake.email@example.com"}
    assert delete_person_from_db(p) is None

    # Now let's update p to have the id key-value pair. But this id does not exist in
    # the database
    mocker.patch(
        "api.resources.http_methods.get.get_person_by_id",
        return_value=None,
    )
    p["id"] = "a-person-with-this-id-does-not-exist"
    assert delete_person_from_db(p) is None

    # Now let's update p to have the id key-value pair, with this id existing in
    # the database
    mocker.patch(
        "api.resources.http_methods.get.get_person_by_id",
        return_value={
            "id": person[0],
            "full_name": person[1],
            "phone_number": person[2],
        },
    )
    p["id"] = person[0]
    assert delete_person_from_db(p) == {
        "id": person[0],
        "full_name": person[1],
        "phone_number": person[2],
    }

    # Validate that this person no longer exists in the database
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    people = [
        record
        for record in cur.execute(f"SELECT * FROM people WHERE id = '{p.get('id')}'")
    ]
    con.close()

    assert len(people) == 0

    # Add this person back into the database as this was only a test (undo side effects)
    post_person_to_db(p)
