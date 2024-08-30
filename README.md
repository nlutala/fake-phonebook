# fake-phonebook
A small project creating an API of a phonebook filled with fake people, you can retrieve people, edit people and delete people.

## Getting Started
Please ensure that you have Python version 3 installed on your computer.

You can find the latest version of Python available using this link: https://www.python.org/downloads/

## Installing
* Open your preferred terminal (command prompt, windows powershell etc.) in the directory where this README.md file is located
* Create a virtual environment by writing ``` python -m .venv ``` in the terminal (feel free to look at the venv documentation here: https://docs.python.org/3/library/venv.html)
* Activate the virtual environment writing: ``` source .venv/bin/activate ```
* Now write ``` python pip -r requirements.txt ``` to install the dependencies needed for this project

Now you should have the required libraries to run the project

## Executing the program
* In the terminal, navigate to fake-phonebook/fake_phonebook. Here is where the main program to be run is.
* Write ``` python main.py ``` to run the server on port 8000.

At this point, I would recommend using a tool like [Postman](https://www.postman.com/) to make calls to the Falcon API

### (REST) API Calls

#### Create (POST)
Using the ``` localhost:8000/contacts ``` URI, you can create a new contact in the fake-phonebook.

This route accepts a ``` {name: NAME, phone_number: PHONE_NUMBER} ``` JSON (or dictionary) in the body of the call, where:

* NAME is a string containing a name of a person or company you would like to store in the phonebook and;
* PHONE_NUMBER is a string containing the phone number you would like to store in the phonebook.

#### Read (GET)
Using the ``` localhost:8000/contacts ``` URI, you can get all the contacts in the fake-phonebook.

You can also use the ``` localhost:8000/contacts/CONTACT_ID ``` URI to get the name and phone number of a contact in the phonebook as a JSON (or dictionary), where:

* CONTACT_ID is a string containing the id of a contact in the phonebook.

#### Update (PUT)
Using the ``` localhost:8000/contacts/CONTACT_ID ``` URI, you can update the name and/or phone number of a specific contact in the fake-phonebook, where:

* CONTACT_ID is a string containing the id of a contact in the phonebook.

This route accepts:
* ``` {name: NAME, phone_number: PHONE_NUMBER} ``` JSON (or dictionary) in the body of the call or,
* ``` {name: NAME} ``` JSON (or dictionary) in the body of the call or,
* ``` {phone_number: PHONE_NUMBER} ``` JSON (or dictionary) in the body of the call

Where:
* NAME is a string containing the new name of a person or company you would like to store under the contact with the CONTACT_ID in the phonebook and;
* PHONE_NUMBER is a string containing the new phone number you would like to store under the contact with the CONTACT_ID in the phonebook.

#### Delete (DELETE)
Using the ``` localhost:8000/contacts/CONTACT_ID ``` URI, you can delete a specific contact in the fake-phonebook, where:

* CONTACT_ID is a string containing the id of the contact you would like to delete in the phonebook.

### Seeding the database
If you ever need more people in the phonebook (for one reason or another), you can:
* navigate to fake-phonebook/fake_phonebook in the terminal
* write ``` python generate_fake_contact_data.py ``` and press the enter key

By default, this will insert another 1000 contacts into the phonebook. If you would like to change the amount of contacts added to the phonebook, you can change the integer value in ``` /fake-phonebook/fake_phonebook/generate_fake_contact_data.py ``` on line 16 to however many contacts you would like to add to the phonebook.

## Author
Nathan Lutala, nlutala

## Version History
* 0.1 - First release

## Acknowledgements
Inspiration for writing this readme file

* https://github.com/nlutala/python-basics/
