import json
from random import choice

import falcon
import falcon.media
import pytest
from api.resources.http_methods.delete import delete_contact_from_db
from api.resources.http_methods.get import get_contact_by_id, get_contacts
from api.resources.http_methods.post import post_contact_to_db
from falcon import testing
from main import app


@pytest.fixture
def client():
    return testing.TestClient(app)


# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_post_contact(client):
    """
    Test the post contact operation.
    """
    # Use case 1: Test that on post of a dictionary with no name or phone_number
    # key-value pair returns status code 400.
    contact = {"email_address": "example@example.com"}
    response = client.simulate_post("/contacts", body=json.dumps(contact))
    assert response.status == falcon.HTTP_400

    # Use case 2: Test that on post of a dictionary with only name and no phone_number
    # key-value pair returns status code 400.
    contact["name"] = "Test Post Contact"
    response = client.simulate_post("/contacts", body=json.dumps(contact))
    assert response.status == falcon.HTTP_400

    # Use case 3: Test that on post of a dictionary with no name and just a phone_number
    # key-value pair returns status code 400.
    del contact["name"]

    contact["phone_number"] = "+44 5361237462"
    response = client.simulate_post("/contacts", body=json.dumps(contact))
    assert response.status == falcon.HTTP_400

    # Use case 4: Test that on post of a dictionary with a name and a phone_number
    # key-value pair returns status code 201.
    contact["name"] = "Test Post Contact"
    response = client.simulate_post("/contacts", body=json.dumps(contact))

    assert response.status == falcon.HTTP_201

    contact_id = response.text.split(":")[1].strip()
    assert response.text == (
        f"{contact.get('name')} was added to the phonebook with the "
        f"following id: {contact_id}"
    )

    # Assert that this test contact has actually been added to the phonebook (database)
    assert get_contact_by_id(contact_id) == {
        "id": contact_id,
        "name": contact.get("name"),
        "phone_number": contact.get("phone_number"),
    }

    # Delete "Test Post Contact" from the database
    delete_contact_from_db(
        {
            "id": contact_id,
            "name": contact.get("name"),
            "phone_number": contact.get("phone_number"),
        }
    )
    assert get_contact_by_id(contact_id) is None


def test_get_contact(client):
    """
    Test that getting a contact by their id returns status code 200 (or OK), if the
    id is in the phonebook (or 404 otherwise)
    """
    # Use case when the id is of a contact in the phonebook
    contact = choice(get_contacts())
    response = client.simulate_get(f"/contacts/{contact.get('id')}")
    assert response.status == falcon.HTTP_OK

    # Use case when the id is not of a contact in the phonebook
    response = client.simulate_get("/contacts/this-is-not-a-contact-s-id")
    assert response.status == falcon.HTTP_404


def test_get_contacts(client):
    """
    Test that getting all contacts returns status code 200 (or OK)
    """
    # Use case 1: Without any query parameters
    response = client.simulate_get(f"/contacts")
    assert response.status == falcon.HTTP_OK

    # Use case 2: With a non-supported query parameter (should have the same
    # functionality as Use case 1)
    response = client.simulate_get(f"/contacts?starts_with=Adam+D")
    assert response.status == falcon.HTTP_OK

    # Use case 2: With the supported query parameter of name_starts_with
    response = client.simulate_get(f"/contacts?name_starts_with=Adam+D")
    assert response.status == falcon.HTTP_OK


def test_put_by_id(client):
    """
    Test that you can update a contact by their id.
    """
    # Use case 1: Trying to update a contact's name and phone number when their id
    # doesn't exist in the phonebook should return status code 400.
    response = client.simulate_put(
        "/contacts/this-id-does-not-exist",
        body=json.dumps({"name": "Test Put Contact", "phone_number": "+44 5361237462"}),
    )
    assert response.status == falcon.HTTP_400

    # Use case 2: Trying to update a contact that exists in the phonebook, but an
    # updated name or phone_number is not given should return status code 400.
    contact_id = post_contact_to_db(
        {"name": "Test Contact", "phone_number": "+44 53612374622"}
    )

    response = client.simulate_put(
        f"/contacts/{contact_id}",
        body=json.dumps({"email_address": "example@example.com"}),
    )
    assert response.status == falcon.HTTP_400

    # Use case 3: Trying to update a contact that exists in the phonebook, by only
    # supplying an updated name should return status code 201.
    response = client.simulate_put(
        f"/contacts/{contact_id}",
        body=json.dumps({"name": "Test Put Contact"}),
    )
    assert response.status == falcon.HTTP_201
    assert get_contact_by_id(contact_id)["name"] == "Test Put Contact"

    # Use case 4: Trying to update a contact that exists in the phonebook, by only
    # supplying an updated phone_number should return status code 201.
    response = client.simulate_put(
        f"/contacts/{contact_id}",
        body=json.dumps({"phone_number": "+44 5361237462"}),
    )
    assert response.status == falcon.HTTP_201
    assert get_contact_by_id(contact_id)["name"] == "Test Put Contact"
    assert get_contact_by_id(contact_id)["phone_number"] == "+44 5361237462"

    # Use case 5: Trying to update a contact that exists in the phonebook, by
    # supplying both an updated name and phone_number should return status code 201.
    response = client.simulate_put(
        f"/contacts/{contact_id}",
        body=json.dumps({"name": "Test Contact", "phone_number": "+44 5361237461"}),
    )
    assert response.status == falcon.HTTP_201
    assert get_contact_by_id(contact_id)["name"] == "Test Contact"
    assert get_contact_by_id(contact_id)["phone_number"] == "+44 5361237461"

    # Delete test contact from the phonebook
    delete_contact_from_db(
        {
            "id": contact_id,
            "name": "Test Contact",
            "phone_number": "+44 5361237461",
        }
    )
    assert get_contact_by_id(contact_id) is None


def test_delete_by_id(client):
    """
    Test that you can delete a contact by their id.
    """
    # Use case 1: Assert when you call the contacts/{contact_id} route on an id that
    # doesn't exist in the phonebook, the api should return status code 404.
    response = client.simulate_delete("/contacts/invalid-id")
    assert response.status == falcon.HTTP_404

    # Use case 2: Assert when you call the contacts/{contact_id} route on an id that
    # does exist in the phonebook, the api should return status code 201.
    contact_id = post_contact_to_db(
        {"name": "Test Contact", "phone_number": "+44 53612374622"}
    )

    response = client.simulate_delete(f"/contacts/{contact_id}")
    assert response.status == falcon.HTTP_201


def test_delete_contacts(client):
    """
    Test that you can delete a contact by supplying a list of ids in the body of the
    api call.
    """
    # Use case 1: Assert when you call the delete operation on the contacts/ route with
    # no id key-value pairs, the api should return status code 400.
    response = client.simulate_delete(
        "/contacts",
        body=json.dumps(
            [
                {"email_address": "example@example.com"},
                {"company": "Google"},
                {"fax": "32567939849"},
            ]
        ),
    )
    assert response.status == falcon.HTTP_400

    # Use case 2: Assert when you call the delete operation on the contacts/ route with
    # ids that don't exist in the phonebook, the api should return status code 400.
    contact_id_1 = post_contact_to_db(
        {"name": "Test Contact 1", "phone_number": "+44 5361237462"}
    )
    contact_id_2 = post_contact_to_db(
        {"name": "Test Contact 2", "phone_number": "+44 5361237463"}
    )
    contact_id_3 = post_contact_to_db(
        {"name": "Test Contact 1", "phone_number": "+44 5361237464"}
    )

    response = client.simulate_delete(
        "/contacts",
        body=json.dumps(
            [{"id": "invalid-id-1"}, {"id": "invalid-id-2"}, {"id": "invalid-id-3"}]
        ),
    )
    assert response.status == falcon.HTTP_400

    # Use case 3: Assert when you call the delete operation on the contacts/ route with
    # ids that do exist in the phonebook, the api should return status code 201.
    response = client.simulate_delete(
        "/contacts",
        body=json.dumps(
            [{"id": contact_id_1}, {"id": contact_id_2}, {"id": contact_id_2}]
        ),
    )
    assert response.status == falcon.HTTP_201
    assert get_contact_by_id(contact_id_1) is None
    assert get_contact_by_id(contact_id_2) is None
    assert get_contact_by_id(contact_id_3) is None
