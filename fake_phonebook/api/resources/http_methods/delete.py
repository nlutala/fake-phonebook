import sqlite3

from api.resources.helpers.env import PATH_TO_DB
from api.resources.http_methods.get import get_contact_by_id


def delete_contact_from_db(contact_data: dict[str, str]) -> dict[str, str] | None:
    """
    Takes a dictionary with a contact's id and deletes this from the database.\n

    :param - contact_data (a dictionary of a contact's id as a key-value pair)\n

    Returns the id, name and phone_number of the contact removed from the database
    if the contact exists in the db and they were deleted from the db without an issue.
    Returns None if otherwise.
    """
    # Check that an id key-value pair was given. If not, return None
    if contact_data.get("id") is None:
        return None

    # Check that a contact with this id exists in the database. If not, return None.
    contact_to_delete = get_contact_by_id(contact_data.get("id"))

    if contact_to_delete is None:
        return None

    # Now delete this contact from the database
    with sqlite3.connect(PATH_TO_DB) as con:
        cur = con.cursor()
        cur.execute(f"delete from contacts where id = '{contact_data.get('id')}'")
        con.commit()

    return contact_to_delete


def delete_contacts_from_db(
    contacts_data: list[dict[str, str]]
) -> list[dict[str, str]] | None:
    """
    Takes a list of dictionaries with a contact's id and deletes this from the
    database.\n

    :param - contacts_data (a list of dictionaries of contacts denoted by an id as a
    key-value pair)\n

    Returns a list of the contacts removed as dictionaries with their id, name and,
    phone_number of the contact removed from the database if the contact exists in the db
    and they were deleted from the db without an issue. Returns None if otherwise.
    """
    # Check that an id key-value pair was given. If not, do not add them to the
    # contacts_to_remove list
    contacts_to_delete = [
        contact for contact in contacts_data if contact.get("id") is not None
    ]

    # If the contacts_to_remove list is empty, return None
    if len(contacts_to_delete) == 0:
        return None

    # Get the contacts who actually exists in the database
    deleted_contacts = [
        get_contact_by_id(contact.get("id"))
        for contact in contacts_to_delete
        if get_contact_by_id(contact.get("id")) is not None
    ]

    # If the deleted_contacts list is empty, return None
    if len(deleted_contacts) == 0:
        return None

    # Create a formatted string of a tuple with all the ids to delete to insert into
    # the delete from table clause
    group_of_ids = ", ".join([f"'{contact.get('id')}'" for contact in deleted_contacts])

    # Now delete these contacts from the database
    with sqlite3.connect(PATH_TO_DB) as con:
        cur = con.cursor()
        cur.execute(f"delete from contacts where id in ({group_of_ids})")
        con.commit()

    return deleted_contacts
