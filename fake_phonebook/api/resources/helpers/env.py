import os

PARENT_DIR = os.path.dirname(__file__).partition("api")[0]
PATH_TO_DB = os.path.join(PARENT_DIR, "fake_contacts.db")
