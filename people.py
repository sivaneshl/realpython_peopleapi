from datetime import datetime
from flask import make_response, abort

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:S"))


# Data to serve with our API
PEOPLE = {
    "Farrel": {
        "fname": "Doug",
        "lname": "Farrel",
        "timestamp": get_timestamp()
    },
    "Brockman": {
        "fname": "Kent",
        "lname": "Brockman",
        "timestamp": get_timestamp()
    },
    "Easter": {
        "fname": "Bunny",
        "lname": "Easter",
        "timestamp": get_timestamp()
    }
}

# Create a handler for read (GET) people
# From the swagger documentation OperationId people.readall for Get
def read_all():
    """
    This function responds to the request for /api/people/ with
    the complete list of people

    :return:    sorted list of people
    """
    # Create the list of people from our data
    return [PEOPLE[key] for key in sorted(PEOPLE.keys())]


def read_one(lname):
    """
    This function responds to the request for /api/people/{lname}
    with the matching people from the list

    :param lname:  Last name of the person to find
    :return:    person matching the last name
    """
    # Does the person exist in people
    if lname in PEOPLE:
        person = PEOPLE.get(lname)

    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )

    return person


def create(person):
    """
    This function creates a new person in the people list based on the passed in person data

    :param person:  person to create in the people list
    :return:    201 on success, 406 on person exist
    """
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    # does the person exist already
    if lname not in PEOPLE and lname is not None:
        PEOPLE[lname] = {
            "lname": lname,
            "fname": fname,
            "timestamp": get_timestamp()
        }
        return make_response(
            "{lname} successfully created".format(lname=lname), 201
        )

    else:
        abort(
            406, "Person with last name {lname} already exists".format(lname=lname)
        )


def update(lname, person):
    """
    This function updates an existing person in the people list

    :param lname: last name of the person to update in the people list
    :param person:  person to update
    :return: updated person structure
    """
    # Does the person exist in the people list
    if lname in PEOPLE:
        PEOPLE[lname]["fname"] = person.get("fname")
        PEOPLE[lname]["timestamp"] = get_timestamp()
        return PEOPLE[lname]

    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )


def delete(lname):
    """
    This function deletes a person from the people list

    :param lname: last name of the person to delete
    :return: 200 on successful delete, 404 if not found
    """
    # Does this person exist in the list
    if lname in PEOPLE:
        del PEOPLE[lname]
        return make_response(
            "{lname} successfully deleted".format(lname=lname), 200
        )

    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )