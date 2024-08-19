"""
A module that returns a list of people in the database created after running the
create_and_load_data.py
"""

import os
import sqlite3
from uuid import uuid4


def get_people() -> list[dict[str, str]]:
    """
    Returns a list of people and their phone number in the phonebook ordered in
    alphabetical order (a-z)
    """

    parent_dir = os.path.dirname(__file__).partition("api")[0]
    path_to_db = os.path.join(parent_dir, "fake_people.db")
    con = sqlite3.connect(path_to_db)
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

    parent_dir = os.path.dirname(__file__).partition("api")[0]
    path_to_db = os.path.join(parent_dir, "fake_people.db")
    con = sqlite3.connect(path_to_db)
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


def add_people_to_db(person_row: list[tuple]) -> int:
    """
    Writes data about fake people from a list of tuples (where each tuple is a person's
    record) to a database \n

    :param - person-row (tuple) - the tuple representing the rows of a person to write
    to the database.\n

    returns the number of rows written to the database
    """

    # Set initially to False as we will then check if the fake_people.db already exists
    parent_dir = os.path.dirname(__file__).partition("api")[0]
    only_insert = True if "fake_people.db" in os.listdir(parent_dir) else False

    # Create a database called fake_people
    path_to_db = os.path.join(parent_dir, "fake_people.db")
    con = sqlite3.connect(path_to_db)
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
        print(people_to_insert)
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
