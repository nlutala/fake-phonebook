from wsgiref.simple_server import make_server

import falcon
from api.resources.phonebook_resource import PhonebookResource

# falcon.App instances are callable WSGI apps
# in larger applications the app is created in a separate file
app = falcon.App()

# Resources are represented by long-lived class instances
people = PhonebookResource()

# Supported operations are: Create (POST), Read (GET - everyone in the resource),
# Delete (DELETE - multiple people)
app.add_route("/people", people)

# Supported operations are: Read (GET - a single person in the resource), Update (PUT),
# Delete (DELETE - a single person)
app.add_route("/people/{person_id}", people, suffix="by_id")


if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")

        # Serve until process is killed
        httpd.serve_forever()
