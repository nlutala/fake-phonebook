from wsgiref.simple_server import make_server

import falcon
from api.resources.phonebook_resource import PhonebookResource

# falcon.App instances are callable WSGI apps
# in larger applications the app is created in a separate file
app = falcon.App()

# Resources are represented by long-lived class instances
people = PhonebookResource()

# Post methods (Create)
app.add_route("/people/add_person", people)

# Get methods (Read)
app.add_route("/people", people, suffix="all")
app.add_route("/people/{person_id}", people, suffix="by_id")
app.add_route("/people/name_starts_with={letter_or_name}", people, suffix="starts_with")

# Update method (Update)
app.add_route("/people/edit_person", people)

# Delete method (Delete)
app.add_route("/people/remove_person", people, suffix="by_id")
app.add_route("/people/remove_people", people)


if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")

        # Serve until process is killed
        httpd.serve_forever()
