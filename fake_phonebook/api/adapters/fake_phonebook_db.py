"""
The class used to interact with the database
"""

import os
import sqlite3

from api.adapters.env import PARENT_DIR, PATH_TO_DB


class FakePhonebookDatabase:
    def __init__(self, path_to_db=PATH_TO_DB) -> None:
        self.path_to_db = path_to_db

    def _connect(self) -> sqlite3.Connection:
        """
        Establish a connection to the database using the self.path_to_db
        """
        if "fake_people.db" not in os.listdir(PARENT_DIR):
            con = self._create_db(self, sqlite3.connect(self.path_to_db))
            return con

        return sqlite3.connect(self.path_to_db)

    def _create_db(self, connection: sqlite3.Connection) -> None:
        cur = connection.cursor()
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
        connection.commit()

    def select(self, what_to_select=["*"], where_clause="") -> list[dict[str, str]]:
        """
        Formats and executes select statements to the db.\n

        :param - what_to_select (list[str] e.g. ["phone_number", "full_name"])\n

        Optional:\n
        :param - where_clause (a string for filtering things from the database i.e.
        "WHERE id = 'person_id'")
        """
        con = self._connect()
        cur = con.cursor()

        if what_to_select == ["*"]:
            select_statement = "SELECT id, full_name, phone_number FROM people"
        else:
            select_statement = f"SELECT {', '.join(what_to_select)} FROM people"

        if where_clause != "":
            select_statement += f" {where_clause}"

        select_statement += " order by full_name"

        if what_to_select == ["*"]:
            people = [
                {
                    "id": person[0],
                    "full_name": person[1],
                    "phone_number": person[2],
                }
                for person in cur.execute(select_statement)
            ]
        else:
            people = []
            people_from_db = cur.execute(select_statement)

            for p in people_from_db:
                person = {}
                for i in range(len(p)):
                    person[what_to_select[i]] = p[i]

                people.append(person)

        con.close()
        return people

    def select_starting_with(self, starting_string: str) -> list[dict[str, str]]:
        """
        Formats and executes select a statement to the db with a name starting with
        a specific string.\n

        :param - starting_string (a string for filtering things from the database i.e.
        "WHERE id = 'person_id'")
        """
        con = self._connect()
        cur = con.cursor()

        select_statement = f"""
            SELECT id, full_name, phone_number
            FROM people
            WHERE full_name LIKE '{starting_string}%'
            ORDER BY full_name
        """.strip().replace(
            "\n", " "
        )

        people = [
            {
                "id": person[0],
                "full_name": person[1],
                "phone_number": person[2],
            }
            for person in cur.execute(select_statement)
        ]

        con.close()
        return people

    def update(self, set_clause: str, where_clause: str) -> None:
        """
        Formats and executes update statements to the db.\n

        :param - set_clause (a string for what to update i.e.
        "SET phone_number = '+44 7892348212'")\n
        :param - where_clause (a string for specifying what record(s) to update from the
        database i.e. "WHERE id = 'person_id'")
        """
        con = self._connect()
        cur = con.cursor()
        cur.execute(f"UPDATE people {set_clause} {where_clause}")
        con.commit()
        con.close()

    def delete(self, where_clause="") -> None:
        """
        Formats and executes delete statements to the db.\n

        :param - where_clause (a string for specifying what record(s) to delete from the
        database i.e. "WHERE id = 'person_id'")
        """
        con = self._connect()
        cur = con.cursor()
        cur.execute(f"delete from people {where_clause}")
        con.commit()
        con.close()

    def insert(self, people_to_insert: list[tuple[str]]) -> None:
        """
        Formats and executes insert statements to the db.\n

        :param - people_to_insert (a list denoting a record of things specifying what to
        insert into the database)
        """
        con = self._connect()
        cur = con.cursor()
        cur.execute(f"INSERT INTO people VALUES(?, ?, ?, ?, ?, ?, ?)", people_to_insert)
        con.commit()
        con.close()
