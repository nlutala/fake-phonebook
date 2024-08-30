import os
import sqlite3
from uuid import uuid4

from api.resources.helpers.env import PARENT_DIR, PATH_TO_DB


def add_contacts_to_db(contact_row: list[tuple]) -> int:
    """
    Writes data about fake contacts from a list of tuples (where each tuple is a contact's
    record) to a database \n

    :param - contact-row (tuple) - the tuple representing the rows of a contact to write
    to the database.\n

    returns the number of rows written to the database
    """
    # Set initially to False as we will then check if the fake_contacts.db already exists
    only_insert = True if "fake_contacts.db" in os.listdir(PARENT_DIR) else False

    # Create a database called fake_contacts
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()

    if only_insert is False:
        # Create the table in the fake_contacts database
        cur.execute(
            """
            CREATE TABLE contacts(
                id,
                name,
                phone_number
            )
            """
        )

    # Check whether the contact already exists in the db before inserting them
    contacts_in_the_db = 0
    contacts_to_insert = []
    for record in contact_row:
        temp_result = [
            row
            for row in cur.execute(f"SELECT * FROM contacts WHERE name = '{record[1]}'")
        ]

        if len(temp_result) != 0:
            contacts_in_the_db += 1
        else:
            contacts_to_insert.append(tuple(record))

    if len(contacts_to_insert) != 0:
        # Insert the data about the fake contacts from the tuple into the table
        cur.executemany("INSERT INTO contacts VALUES(?, ?, ?)", contacts_to_insert)
        con.commit()
        con.close()

    return len(contacts_to_insert)


def post_contact_to_db(contact_data: dict[str, str]) -> str | None:
    """
    Takes a dictionary with a contact's name and phone_number and loads this
    to the database.\n

    :param - contact_data (a dictionary consisting of a name, phone_number key,
    value pair)\n

    Returns the id of the contact if the contact doesn't exist in the db and they were
    able to be inserted into the db without an issue. Returns None if otherwise.
    """
    # When someone using the api posts a new contact to add to the phonebook, I want to
    # enforce that they've added a "name" and "phone_number" (key, value) pair

    if contact_data.get("name") is None or len((contact_data).get("name")) == 0:
        return None

    if contact_data.get("phone_number") is None or len((contact_data).get("name")) == 0:
        return None

    contact_data["id"] = str(uuid4())

    contact_record = [
        (contact_data["id"], contact_data["name"], contact_data["phone_number"]),
    ]

    if add_contacts_to_db(contact_record) != 0:
        return contact_data["id"]

    return None
