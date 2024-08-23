"""
A resource that users can call to retrieve all the people in the phonebook
"""

from json import dumps, loads

import falcon
from api.resources.helpers.list_people import (
    delete_people_from_db,
    delete_person_from_db,
    get_people,
    get_people_starting_with,
    get_person_by_id,
    post_person_to_db,
    update_person_in_db,
)


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class PhonebookResource:
    # Post methods (Create)
    def on_post(self, req, resp):
        """
        Handles a POST request for adding a new entry into the phonebook.\n
        {full_name, phone_number}
        """
        req.content_type = falcon.MEDIA_JSON
        person_data = loads(dumps(req.media))

        person_id = post_person_to_db(person_data)

        if person_id is None:
            resp.status = falcon.HTTP_400
            resp.text = (
                "Bad request. Please ensure that the 'full_name' and "
                "'phone_number' key-value pairs are present and that this new "
                "person you would like to the phonebook does not currently "
                "exist in the phonebook."
            )
        else:
            resp.status = falcon.HTTP_201
            resp.text = (
                f"{person_data.get('full_name')} was added to the phonebook with the "
                f"following id: {person_id}"
            )

    # Get methods (Read)
    def on_get_all(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_JSON
        resp.media = get_people()

    def on_get_by_id(self, req, resp, person_id: str):
        """Handles a GET request for a specific person"""
        resp.content_type = falcon.MEDIA_JSON

        if get_person_by_id(person_id) is None:
            resp.status = falcon.HTTP_404
            resp.text = f"Person with id: '{person_id}' was not found.\n"
        else:
            resp.status = falcon.HTTP_200
            resp.media = get_person_by_id(person_id)

    def on_get_starts_with(self, req, resp, letter_or_name: str):
        """
        Handles a GET request to retrieve people in the phonebook who's name starts with
        a chosen string.
        """
        resp.content_type = falcon.MEDIA_JSON

        if get_people_starting_with(letter_or_name) is None:
            resp.status = falcon.HTTP_404
            resp.text = (
                f"There is no one in the phonebook whose name starts with "
                f"'{letter_or_name}'\n"
            )
        else:
            resp.status = falcon.HTTP_200
            resp.media = get_people_starting_with(letter_or_name)

    # Update method (Update)
    def on_put(self, req, resp):
        """
        Handles a PUT request for updating information about someone in the phonebook
        (either full_name or phone_number).\n
        The user of the api will receive a message saying that a person (identified by
        their id is has a (new) full_name and (new) phone number.
        """
        req.content_type = falcon.MEDIA_JSON
        person_data = loads(dumps(req.media))

        updated_person = update_person_in_db(person_data)

        if updated_person is None:
            resp.status = falcon.HTTP_400
            resp.text = (
                "Bad request. Please ensure that the 'id', 'full_name' and "
                "'phone_number' key-value pairs are present and that this person you "
                "would like to update the details of exists in the phonebook. "
            )
        else:
            resp.status = falcon.HTTP_201
            resp.text = (
                f"The person with an id of {updated_person.get('id')} was updated to "
                f"be called {updated_person.get('full_name')}, with a phone number of: "
                f"{updated_person.get('phone_number')}"
            )

    # Delete method (Delete)
    def on_delete_by_id(self, req, resp):
        """
        Handles a DELETE request for deleting an entry in the phonebook.\n
        The user of the api will receive a message saying that a person (identified by
        their name and phone number) has been removed from the phonebook.
        """
        req.content_type = falcon.MEDIA_JSON
        person_data = loads(dumps(req.media))

        deleted_data = delete_person_from_db(person_data)

        if deleted_data is None:
            resp.status = falcon.HTTP_400
            resp.text = (
                "Bad request. Please ensure that the id of the person you would like "
                "to remove is given as a key-value pair, and that this id already "
                "exists in the phonebook."
            )
        else:
            resp.status = falcon.HTTP_201
            resp.text = (
                f"A person, called {deleted_data.get('full_name')}, with a phone number "
                f"of '{deleted_data.get('phone_number')}' has been removed from the "
                "phonebook."
            )

    def on_delete(self, req, resp):
        """
        Handles a DELETE request for deleting multiple entries in the phonebook.\n
        The user of the api will receive a message listing the people (identified by
        their name and phone number) have been removed from the phonebook.
        """
        req.content_type = falcon.MEDIA_JSON
        people_data = loads(dumps(req.media))

        deleted_data = delete_people_from_db(people_data)

        if deleted_data is None:
            resp.status = falcon.HTTP_400
            resp.text = (
                "Bad request. Please ensure that you have supplied a list of ids of "
                "the people you would like to remove is given as key-value pairs, and "
                "that these ids already exist in the phonebook."
            )
        else:
            resp.status = falcon.HTTP_201
            part_of_response = ""
            for person in deleted_data:
                part_of_response += (
                    f"A person, called {person.get('full_name')}, with a phone number "
                    f"of '{person.get('phone_number')}' has been removed from the "
                    "phonebook.\n"
                )

            resp.text = part_of_response
