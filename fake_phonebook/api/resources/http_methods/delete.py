import sqlite3

from api.resources.helpers.env import PATH_TO_DB
from api.resources.http_methods.get import get_person_by_id


def delete_person_from_db(person_data: dict[str, str]) -> dict[str, str] | None:
    """
    Takes a dictionary with a person's id and deletes this from the database.\n

    :param - person_data (a dictionary of a person's id as a key-value pair)\n

    Returns the id, full_name and phone_number of the person removed from the database
    if the person exists in the db and they were deleted from the db without an issue.
    Returns None if otherwise.
    """
    # Check that an id key-value pair was given. If not, return None
    if person_data.get("id") is None:
        return None

    # Check that a person with this id exists in the database. If not, return None.
    person_to_delete = get_person_by_id(person_data.get("id"))

    if person_to_delete is None:
        return None

    # Now delete this person from the database
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    cur.execute(f"delete from people where id = '{person_data.get('id')}'")
    con.commit()
    con.close()

    return person_to_delete


def delete_people_from_db(
    people_data: list[dict[str, str]]
) -> list[dict[str, str]] | None:
    """
    Takes a list of dictionaries with a person's id and deletes this from the
    database.\n

    :param - people_data (a list of dictionaries of people denoted by an id as a
    key-value pair)\n

    Returns a list of the people removed as dictionaries with their id, full_name and,
    phone_number of the person removed from the database if the person exists in the db
    and they were deleted from the db without an issue. Returns None if otherwise.
    """
    # Check that an id key-value pair was given. If not, do not add them to the
    # people_to_remove list
    people_to_delete = [
        person for person in people_data if person.get("id") is not None
    ]

    # If the people_to_remove list is empty, return None
    if len(people_to_delete) == 0:
        return None

    # Get the people who actually exists in the database
    deleted_people = [
        get_person_by_id(person.get("id"))
        for person in people_to_delete
        if get_person_by_id(person.get("id")) is not None
    ]

    # If the deleted_people list is empty, return None
    if len(deleted_people) == 0:
        return None

    # Create a formatted string of a tuple with all the ids to delete to insert into
    # the delete from table clause
    group_of_ids = ", ".join([f"'{person.get('id')}'" for person in deleted_people])

    # Now delete these people from the database
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    cur.execute(f"delete from people where id in ({group_of_ids})")
    con.commit()
    con.close()

    return deleted_people
