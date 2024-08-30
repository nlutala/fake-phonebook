"""
The main .py file to run which creates records of fake contacts, and writes these
records of fake people from the .csv file to a database.

Author: nlutala (Nathan Lutala)
"""

import logging
import os
import sqlite3

from create_and_load.fake_contacts.fake_contact_records import get_contacts

# Python Basics: Python scope and LEGB rule
# Global variables
NUM_OF_PEOPLE_TO_GENERATE = 1000
LOGGER = logging.getLogger(__name__)

"""
Letting the logger know to write all logs at the info level (my logs) and above to a
file called create_and_load_data.log
"""
logging.basicConfig(
    filename="generate_fake_contact_data.log",
    filemode="w",  # To write new content every time the program is run again
    encoding="utf-8",
    level=logging.INFO,
)


if __name__ == "__main__":
    # Step 1 - Create data about fake contacts
    contacts = get_contacts(NUM_OF_PEOPLE_TO_GENERATE)

    # Step 2 - Check if the database already exists
    # If it does, just insert the new values into the database
    # If not, create the database, table and insert into the table
    parent_dir = os.path.dirname(__file__).partition("create_and_load")[0]
    path_to_db = os.path.join(parent_dir, "fake_contacts.db")

    if "fake_contacts.db" not in os.listdir(parent_dir):
        con = sqlite3.connect(path_to_db)
        cur = con.cursor()
        cur.execute(
            """
            CREATE TABLE contacts(
                id,
                name,
                phone_number
            )
            """
        )

    # Step 3 - For i in range(NUM_CONTACTS_TO_GENERATE) write contact to the db
    con = sqlite3.connect(path_to_db)
    cur = con.cursor()
    cur.executemany("INSERT INTO contacts VALUES(?, ?, ?)", contacts)
    con.commit()
    con.close()

    LOGGER.info(f"Wrote {NUM_OF_PEOPLE_TO_GENERATE} rows to the database.")
