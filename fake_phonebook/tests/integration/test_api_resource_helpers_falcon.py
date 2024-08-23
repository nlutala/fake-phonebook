from unittest.mock import Mock

from pytest_mock import mocker


def test_delete_people_from_db(mocker: Mock):
    """
    api.resources.helpers.list_people.delete_people_from_db() should return a list of
    dictionaries consisting the id, full_name and phone_number of the people deleted
    from the database as key-value pairs or None if the people could not be deleted
    from the database successfully.
    """
    pass  # Needs to be an integration test (will do with falcon)
