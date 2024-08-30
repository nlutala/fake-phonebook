from wsgiref.simple_server import make_server

import falcon
from api.resources.contacts import Contacts

# falcon.App instances are callable WSGI apps
# in larger applications the app is created in a separate file
app = falcon.App()

# Resources are represented by long-lived class instances
contacts = Contacts()

# Supported operations are: Create (POST), Read (GET - every one in the resource),
# Delete (DELETE - multiple contacts)
app.add_route("/contacts", contacts)

# Supported operations are: Read (GET - a single contact in the resource), Update (PUT),
# Delete (DELETE - a single contact)
app.add_route("/contacts/{contact_id}", contacts, suffix="by_id")


if __name__ == "__main__":
    with make_server("", 8000, app) as httpd:
        print("Serving on port 8000...")

        # Serve until process is killed
        httpd.serve_forever()
