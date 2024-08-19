"""
A resource that users can call to retrieve all the people in the phonebook
"""

from json import dumps, loads

import falcon
from resources.helpers.list_people import (
    get_people,
    get_person_by_id,
    post_person_to_db,
)


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class PhonebookResource:
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
