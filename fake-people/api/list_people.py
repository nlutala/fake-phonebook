"""
A module that returns a list of people in the database created after running the
create_and_load_data.py
"""

import os
import sqlite3


def get_people_names() -> list[str]:
    """
    Returns a list of people in the phonebook ordered in alphabetical order (a-z)
    """

    path_to_db = os.path.join(os.pardir, "fake_people.db")
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    people_names = [
        full_name[0] for full_name in cur.execute("SELECT full_name FROM people")
    ]
    con.close()

    return sorted(people_names)
