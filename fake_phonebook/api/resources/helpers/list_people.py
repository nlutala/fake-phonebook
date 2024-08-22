"""
A module that returns a list of people in the database created after running the
create_and_load_data.py
"""

import os
import sqlite3
from uuid import uuid4

from resources.helpers.env import PARENT_DIR, PATH_TO_DB


# =============================== CREATE Operations ===================================
def add_people_to_db(person_row: list[tuple]) -> int:
    """
    Writes data about fake people from a list of tuples (where each tuple is a person's
    record) to a database \n

    :param - person-row (tuple) - the tuple representing the rows of a person to write
    to the database.\n

    returns the number of rows written to the database
    """
    # Set initially to False as we will then check if the fake_people.db already exists
    only_insert = True if "fake_people.db" in os.listdir(PARENT_DIR) else False

    # Create a database called fake_people
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()

    if only_insert is False:
        # Create the table in the fake_people database
        cur.execute(
            """
            CREATE TABLE people(
                id,
                full_name,
                first_name,
                last_name,
                email_address,
                phone_number,
                linkedin_profile
            )
            """
        )

    # Check whether the person already exists in the db before inserting them
    people_in_the_db = 0
    people_to_insert = []
    for record in person_row:
        temp_result = [
            row
            for row in cur.execute(
                f"SELECT * FROM people WHERE full_name = '{record[1]}'"
            )
        ]

        if len(temp_result) != 0:
            people_in_the_db += 1
        else:
            people_to_insert.append(tuple(record))

    if len(people_to_insert) != 0:
        # Insert the data about the fake people from the tuple into the table
        cur.executemany(
            "INSERT INTO people VALUES(?, ?, ?, ?, ?, ?, ?)", people_to_insert
        )
        con.commit()
        con.close()

    return len(people_to_insert)


def post_person_to_db(person_data: dict[str, str]) -> str | None:
    """
    Takes a dictionary with a person's full_name and phone_number and loads this
    to the database. It adds the other relevant information (first_name, last_name,
    email_address, linkedin_profile) to the database automatically.\n

    :param - person_data (a dictionary consisting of a full_name, phone_number key,
    value pair)\n

    Returns the id of the person if the person doesn't exist in the db and they were
    able to be inserted into the db without an issue. Returns None if otherwise.
    """
    # When someone using the api posts a new person to add to the phonebook, I want to
    # enforce that they've added a "full_name" and "phone_number" (key, value) pair

    if person_data.get("full_name") is None or len((person_data).get("full_name")) == 0:
        return None

    if (
        person_data.get("phone_number") is None
        or len((person_data).get("full_name")) == 0
    ):
        return None

    person_data["id"] = str(uuid4())
    person_data["first_name"] = person_data.get("full_name").split(" ")[0]
    person_data["last_name"] = " ".join(person_data.get("full_name").split(" ")[1:])
    person_data["email_address"] = (
        f"""{
            person_data.get("first_name").lower()
        }.{
            person_data.get("last_name").lower()
        }@example.com
        """.strip()
    )
    person_data["linkedin_profile"] = (
        f"""
        wwww.linkedin.com/{
            person_data.get("first_name").lower()
        }-{
            person_data.get("last_name").lower()
        }
        """.strip()
    )

    person_record = [
        (
            person_data["id"],
            person_data["full_name"],
            person_data["first_name"],
            person_data["last_name"],
            person_data["email_address"],
            person_data["phone_number"],
            person_data["linkedin_profile"],
        ),
    ]

    if add_people_to_db(person_record) != 0:
        return person_data["id"]

    return None


# ================================= READ Operations ===================================
def get_people() -> list[dict[str, str]]:
    """
    Returns a list of people and their phone number in the phonebook ordered in
    alphabetical order (a-z)
    """
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    people = [
        {
            "id": person[0],
            "full_name": person[1],
            "phone_number": person[2],
        }
        for person in cur.execute(
            "SELECT id, full_name, phone_number FROM people order by full_name"
        )
    ]
    con.close()

    return people


def get_person_by_id(person_id: str) -> dict[str, str] | None:
    """
    Returns a dictionary representing a person by their id, full_name and
    phone_number.\n

    :param - person_id (string)\n

    If a person is not associated with this id, the function returns None.
    """
    con = sqlite3.connect(PATH_TO_DB)
    cur = con.cursor()
    people = [
        {
            "id": person[0],
            "full_name": person[1],
            "phone_number": person[2],
        }
        for person in cur.execute(
            f"""
            SELECT id, full_name, phone_number FROM people WHERE id = '{person_id}'
            """
        )
    ]
    con.close()

    return people[0] if len(people) == 1 else None


def get_people_starting_with(string: str) -> list[dict[str, str]] | None:
    """
    Returns a list of people (id, full_name and phone_number) in the phonebook ordered
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
    people = [
        {
            "id": person[0],
            "full_name": person[1],
            "phone_number": person[2],
        }
        for person in cur.execute(
            f"""
            SELECT id, full_name, phone_number FROM people
            WHERE full_name LIKE '{string}%'
            order by full_name
            """.strip().replace(
                "\n", " "
            )
        )
    ]
    con.close()

    return people if len(people) != 0 else None


# ================================ UPDATE Operations ==================================
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


# ================================= DELETE Operations =================================
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
