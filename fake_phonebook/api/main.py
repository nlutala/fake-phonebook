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
app.add_route("/people", people, suffix="all")
app.add_route("/people/{person_id}", people, suffix="by_id")
app.add_route("/people/person", people)

if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")

        # Serve until process is killed
        httpd.serve_forever()
