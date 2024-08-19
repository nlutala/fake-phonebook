"""
A resource that users can call to retrieve all the people in the phonebook
"""

import falcon
from resources.helpers.list_people import get_people, get_person_by_id


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
