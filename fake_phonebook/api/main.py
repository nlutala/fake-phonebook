# examples/things.py

# Let's get this party started!
from wsgiref.simple_server import make_server

import falcon
from resources.phonebook_resource import PhonebookResource

# falcon.App instances are callable WSGI apps
# in larger applications the app is created in a separate file
app = falcon.App()

# Resources are represented by long-lived class instances
people = PhonebookResource()

# things will handle all requests to the '/people' URL path

# Post methods (Create)
app.add_route("/people/add_person", people)  # add suffix="by_id"
# TODO: Add another post method to add multiple people at once
# app.add_route("/people/add_people", people) --> make this the on_post() method

# Get methods (Read)
app.add_route("/people", people, suffix="all")
app.add_route("/people/{person_id}", people, suffix="by_id")
# TODO: add another get method to get everyone in the db whose first_name starts with
# a letter e.g.
# app.add_route(
# "/people/search?q=first+name+starts+with={letter}", people, suffix="by_first_name"
# )
# TODO: add another get method to get everyone in the db whose last_name starts with
# a letter e.g.
# app.add_route(
# "/people/search?q=last+name+starts+with={letter}", people, suffix="by_last_name"
# )

# Delete method (Delete)
app.add_route("/people/remove_person", people, suffix="by_id")
# TODO: add another delete method to delete multiple people by id (it should take a
# list of dictionaries)
# app.add_route("/people/remove_person", people)


if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")

        # Serve until process is killed
        httpd.serve_forever()
