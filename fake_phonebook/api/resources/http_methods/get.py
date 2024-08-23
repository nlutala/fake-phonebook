import sqlite3

from api.adapters.env import PATH_TO_DB
from api.adapters.fake_phonebook_db import FakePhonebookDatabase


def get_people() -> list[dict[str, str]]:
    """
    Returns a list of people and their phone number in the phonebook ordered in
    alphabetical order (a-z)
    """
    return FakePhonebookDatabase().select(["*"])


def get_person_by_id(person_id: str) -> dict[str, str] | None:
    """
    Returns a dictionary representing a person by their id, full_name and
    phone_number.\n

    :param - person_id (string)\n

    If a person is not associated with this id, the function returns None.
    """
    people = FakePhonebookDatabase().select(["*"], f"WHERE id = '{person_id}'")
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

    people = FakePhonebookDatabase().select_starting_with(string)

    return people if len(people) != 0 else None
