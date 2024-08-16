"""
A module that returns a list of people in the database created after running the
create_and_load_data.py
"""

import os
import sqlite3


def get_people() -> list[str]:
    """
    Returns a list of people and their phone number in the phonebook ordered in
    alphabetical order (a-z)
    """

    parent_dir = os.path.dirname(__file__).partition("api")[0]
    path_to_db = os.path.join(parent_dir, "fake_people.db")
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    people = [
        "{"
        + ", ".join(
            [
                "id: " + person[0],
                "full_name: " + person[1],
                "phone_number: " + person[2],
            ]
        )
        + "}"
        for person in cur.execute(
            """SELECT id, full_name, phone_number FROM people order by full_name"""
        )
    ]
    con.close()

    return people
