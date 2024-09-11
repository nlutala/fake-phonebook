import sqlite3

from api.resources.helpers.env import PATH_TO_DB


def get_contacts(filters={}) -> list[dict[str, str]] | None:
    """
    Returns a list of contacts and their phone number in the phonebook ordered in
    alphabetical order (a-z)

    :param - filters (None by default), but this is for all the query parameters (for
    now, it should only be name)
    """
    sql_query = "SELECT id, name, phone_number FROM contacts"
    where = " WHERE "
    where_clause = []
    order_by_clause = " ORDER BY name"

    if filters != {}:
        for key in filters.keys():
            if key in ["name"]:
                where_clause.append(
                    f"{key.replace('-', '_')} LIKE '{filters.get(key)}%'"
                )

    if where_clause != []:
        sql_query += where + " AND ".join(where_clause)

    sql_query += order_by_clause

    with sqlite3.connect(PATH_TO_DB) as con:
        cur = con.cursor()
        contacts = [
            {
                "id": contact[0],
                "name": contact[1],
                "phone_number": contact[2],
            }
            for contact in cur.execute(f"{sql_query}")
        ]

    return contacts if len(contacts) > 0 else None


def get_contact_by_id(contact_id: str) -> dict[str, str] | None:
    """
    Returns a dictionary representing a contact by their id, name and
    phone_number.\n

    :param - contact_id (string)\n

    If a contact is not associated with this id, the function returns None.
    """
    with sqlite3.connect(PATH_TO_DB) as con:
        cur = con.cursor()
        contacts = [
            {
                "id": contact[0],
                "name": contact[1],
                "phone_number": contact[2],
            }
            for contact in cur.execute(
                f"""
                SELECT id, name, phone_number FROM contacts WHERE id = '{contact_id}'
                """
            )
        ]

    return contacts[0] if len(contacts) == 1 else None
