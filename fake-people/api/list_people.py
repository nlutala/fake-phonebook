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

    path_to_db = os.path.join(os.pardir, "fake_people.db")
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    people = [
        f"{person[0]}: {person[1]}"
        for person in cur.execute("SELECT full_name, phone_number FROM people")
    ]
    con.close()

    return sorted(people)
