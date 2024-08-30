from random import choice

import falcon
import falcon.media
import pytest
from api.resources.http_methods.get import get_contacts
from falcon import testing
from main import app


@pytest.fixture
def client():
    return testing.TestClient(app)


# pytest will inject the object returned by the "client" function
# as an additional parameter.
def test_get_contact(client):
    """
    Test thet getting a contact by their id returns status code 200 (or OK), if the
    id is in the phonebook (or 404 otherwise)
    """
    # Use case when the id is of a contact in the phonebook
    contact = choice(get_contacts())
    response = client.simulate_get(f"/contacts/{contact.get('id')}")
    assert response.status == falcon.HTTP_OK

    # Use case when the id is not of a contact in the phonebook
    response = client.simulate_get(f"/contacts/this-is-not-a-contact-s-id")
    assert response.status == falcon.HTTP_404


def test_get_contacts(client):
    """
    Test thet getting all contacts returns status code 200 (or OK)
    """
    response = client.simulate_get(f"/contacts")
    assert response.status == falcon.HTTP_OK
