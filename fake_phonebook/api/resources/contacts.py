"""
A resource that users can call to retrieve all the contacts in the phonebook
"""

from json import dumps, loads

import falcon
from api.resources.http_methods.delete import (
    delete_contact_from_db,
    delete_contacts_from_db,
)
from api.resources.http_methods.get import get_contact_by_id, get_contacts
from api.resources.http_methods.post import post_contact_to_db
from api.resources.http_methods.update import update_contact_in_db


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class Contacts:
    # Post methods (Create)
    def on_post(self, req, resp):
        """
        Handles a POST request for adding a new entry into the phonebook.\n
        {name, phone_number}
        """
        req.content_type = falcon.MEDIA_JSON
        contact_data = loads(dumps(req.media))

        contact_id = post_contact_to_db(contact_data)

        if contact_id is None:
            resp.status = falcon.HTTP_400
            resp.text = (
                "Bad request. Please ensure that the 'name' and 'phone_number' "
                "key-value pairs are present and that this new contact you would like "
                "to the phonebook does not currently exist in the phonebook."
            )
        else:
            resp.status = falcon.HTTP_201
            resp.text = (
                f"{contact_data.get('name')} was added to the phonebook with the "
                f"following id: {contact_id}"
            )

    # Get methods (Read)
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_JSON
        resp.media = get_contacts(req.params)

    def on_get_by_id(self, req, resp, contact_id: str):
        """Handles a GET request for a specific contact"""
        resp.content_type = falcon.MEDIA_JSON

        if get_contact_by_id(contact_id) is None:
            resp.status = falcon.HTTP_404
            resp.text = f"Contact with id: '{contact_id}' was not found.\n"
        else:
            resp.status = falcon.HTTP_200
            resp.media = get_contact_by_id(contact_id)

    # Update method (Update)
    def on_put_by_id(self, req, resp, contact_id: str):
        """
        Handles a PUT request for updating information about someone in the phonebook
        (either name or phone_number).\n
        The user of the api will receive a message saying that a contact (identified by
        their id is has a (new) name and (new) phone number.
        """
        req.content_type = falcon.MEDIA_JSON
        contact_data = loads(dumps(req.media))
        contact_data["id"] = contact_id

        updated_contact = update_contact_in_db(contact_data)

        if updated_contact is None:
            resp.status = falcon.HTTP_400
            resp.text = (
                "Bad request. Please ensure that the 'name' and 'phone_number' "
                "key-value pairs are present in the body of the api call and that the "
                "contact you would like to update the details of exists in the phonebook. "
            )
        else:
            resp.status = falcon.HTTP_201
            resp.text = (
                f"The contact with an id of {updated_contact.get('id')} was updated to "
                f"be called {updated_contact.get('name')}, with a phone number of: "
                f"{updated_contact.get('phone_number')}"
            )

    # Delete method (Delete)
    def on_delete_by_id(self, req, resp, contact_id: str):
        """
        Handles a DELETE request for deleting an entry in the phonebook.\n
        The user of the api will receive a message saying that a contact (identified by
        their name and phone number) has been removed from the phonebook.
        """
        contact_data = get_contact_by_id(contact_id)

        if contact_data is None:
            resp.status = falcon.HTTP_404
            resp.text = f"Contact with id: {contact_id} was not found."
        else:
            deleted_data = delete_contact_from_db(contact_data)
            resp.status = falcon.HTTP_201
            resp.text = (
                f"A contact, called {deleted_data.get('name')}, with a phone number "
                f"of '{deleted_data.get('phone_number')}' has been removed from the "
                "phonebook."
            )

    def on_delete(self, req, resp):
        """
        Handles a DELETE request for deleting multiple entries in the phonebook.\n
        The user of the api will receive a message listing the contacts (identified by
        their name and phone number) have been removed from the phonebook.
        """
        req.content_type = falcon.MEDIA_JSON
        contacts_data = loads(dumps(req.media))

        deleted_data = delete_contacts_from_db(contacts_data)

        if deleted_data is None:
            resp.status = falcon.HTTP_400
            resp.text = (
                "Bad request. Please ensure that you have supplied a list of ids of "
                "the contacts you would like to remove is given as key-value pairs, in "
                "the body of the api call and that these ids exist in the phonebook."
            )
        else:
            resp.status = falcon.HTTP_201
            part_of_response = ""
            for contact in deleted_data:
                part_of_response += (
                    f"A contact, called {contact.get('name')}, with a phone number "
                    f"of '{contact.get('phone_number')}' has been removed from the "
                    "phonebook.\n"
                )

            resp.text = part_of_response
