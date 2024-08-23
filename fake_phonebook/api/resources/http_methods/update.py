import sqlite3

from api.resources.helpers.env import PATH_TO_DB
from api.resources.http_methods.get import get_person_by_id


def update_person_in_db(person_data: dict[str, str]) -> dict[str, str] | None:
    """
    Takes a dictionary with a person's id, full_name and/or phone_number and updates
    this person's details in the database.\n

    :param - person_data (a dictionary of a person's id as a key-value pair)\n

    Returns the id, (new) full_name and (new) phone_number of the person updated in the
    database if the person exists in the db and their details were updated without an
    issue. Returns None if otherwise.
    """
    # Check if the id of the person is given
    if person_data.get("id") is None:
        return None

    # Check if the id of the person exists in the db
    if get_person_by_id(person_data.get("id")) is None:
        return None

    # Check that the full_name and/or phone_number to update is given
    full_name = person_data.get("full_name")
    phone_number = person_data.get("phone_number")

    if [full_name, phone_number] == [None, None]:
        return None

    # Format the SET clause for the UPDATE statement
    set_clause = "SET "
    set_full_name = f"full_name = '{full_name}', " if full_name is not None else ""
    set_phone_number = (
        f"phone_number = '{phone_number}'" if phone_number is not None else ""
    )
    set_clause += set_full_name
    set_clause += set_phone_number
    set_clause = (
        set_clause[: len(set_clause) - 2] if set_clause.endswith(", ") else set_clause
    )

    # Now update the details after confirming that the id, full_name and phone_number
    # were given as key-value pairs
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    cur.execute(f"UPDATE people {set_clause} WHERE id = '{person_data.get('id')}'")
    con.commit()
    con.close()

    return get_person_by_id(person_data.get("id"))
