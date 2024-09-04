import sqlite3

from api.resources.helpers.env import PATH_TO_DB


def get_contacts() -> list[dict[str, str]] | None:
    """
    Returns a list of contacts and their phone number in the phonebook ordered in
    alphabetical order (a-z)
    """
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    contacts = [
        {
            "id": contact[0],
            "name": contact[1],
            "phone_number": contact[2],
        }
        for contact in cur.execute(
            "SELECT id, name, phone_number FROM contacts order by name"
        )
    ]
    con.close()

    return contacts if len(contacts) > 0 else None


def get_contact_by_id(contact_id: str) -> dict[str, str] | None:
    """
    Returns a dictionary representing a contact by their id, name and
    phone_number.\n

    :param - contact_id (string)\n

    If a contact is not associated with this id, the function returns None.
    """
    con = sqlite3.connect(PATH_TO_DB)
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
    con.close()

    return contacts[0] if len(contacts) == 1 else None


def get_contacts_starting_with(string: str) -> list[dict[str, str]] | None:
    """
    Returns a list of contacts (id, name and phone_number) in the phonebook ordered
    in that start with a specific string, in alphabetical order (a-z).
    """
    # We don't care about whether the letter is upper or lowercase as I will just add
    # .lower() to the letter anyway
    string = string.lower().strip()

    # Ensure that the letter is at least 1 character long
    if len(string) < 1:
        return None

    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    contacts = [
        {
            "id": contact[0],
            "name": contact[1],
            "phone_number": contact[2],
        }
        for contact in cur.execute(
            f"""
            SELECT id, name, phone_number FROM contacts
            WHERE name LIKE '{string}%'
            order by name
            """.strip().replace(
                "\n", " "
            )
        )
    ]
    con.close()

    return contacts if len(contacts) != 0 else None
