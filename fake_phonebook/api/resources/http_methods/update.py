import sqlite3

from api.resources.helpers.env import PATH_TO_DB
from api.resources.http_methods.get import get_contact_by_id


def update_contact_in_db(contact_data: dict[str, str]) -> dict[str, str] | None:
    """
    Takes a dictionary with a contact's id, name and/or phone_number and updates
    this contact's details in the database.\n

    :param - contact_data (a dictionary of a contact's id as a key-value pair)\n

    Returns the id, (new) name and (new) phone_number of the contact updated in the
    database if the contact exists in the db and their details were updated without an
    issue. Returns None if otherwise.
    """
    # Check if the id of the contact is given
    if contact_data.get("id") is None:
        return None

    # Check if the id of the contact exists in the db
    if get_contact_by_id(contact_data.get("id")) is None:
        return None

    # Check that the name and/or phone_number to update is given
    name = contact_data.get("name")
    phone_number = contact_data.get("phone_number")

    if [name, phone_number] == [None, None]:
        return None

    # Format the SET clause for the UPDATE statement
    set_clause = "SET "
    set_name = f"name = '{name}', " if name is not None else ""
    set_phone_number = (
        f"phone_number = '{phone_number}'" if phone_number is not None else ""
    )
    set_clause += set_name
    set_clause += set_phone_number
    set_clause = (
        set_clause[: len(set_clause) - 2] if set_clause.endswith(", ") else set_clause
    )

    # Now update the details after confirming that the id, name and phone_number
    # were given as key-value pairs
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    cur.execute(f"UPDATE contacts {set_clause} WHERE id = '{contact_data.get('id')}'")
    con.commit()
    con.close()

    return get_contact_by_id(contact_data.get("id"))
