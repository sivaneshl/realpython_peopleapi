from datetime import datetime
from flask import make_response, abort
from config import db
from models import Person, PersonSchema

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

    :return:    json string of list of people
    """
    # Create the list of people from our data
    people = Person.query.order_by(Person.lname).all()
    # tells SQLAlchemy to query the person database table for all the records,
    # sort them in ascending order (the default sorting order), and return a
    # list of Person Python objects as the variable people

    # Serialize the data for response
    person_schema = PersonSchema(many=True)
    # Create an instance of the PersonSchema, passing it the parameter many=True
    # This tells PersonSchema to expect an interable to serialize, which is what the people variable is
    return person_schema.dump(people)
    # The result is an object having a data attribute, an object containing a people list that can be converted to JSON
    # This is returned and converted by Connexion to JSON as the response to the REST API call


def read_one(person_id):
    """
    This function responds to the request for /api/people/{lname}
    with the matching people from the list

    :param person_id:  Id of the person to find
    :return:    person matching the id
    """
    # Get the person requested
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Did we find a person?
    if person is not None:
        # Serialize the data for the response
        person_schema = PersonSchema()
        return person_schema.dump(person)

    else:
        abort(
            404, "Person with person id {person_id} not found".format(person_id=person_id)
        )


def create(person):
    """
    This function creates a new person in the people list based on the passed in person data

    :param person:  person to create in the people list
    :return:    201 on success, 406 on person exist
    """
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    # Existing person
    existing_person = Person.query.filter(Person.fname==fname).filter(Person.lname==lname).one_or_none()

    # does the person exist already
    if existing_person is None:

        # Create the person instance using the schema and the person data that is passed in
        person_schema = PersonSchema()
        new_person = person_schema.load(person, session=db.session)

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person as response
        data = person_schema.dump(new_person)
        return data, 201
    else:
        abort(
            406, f"Person {fname} {lname} already exists"
        )


def update(person_id, person):
    """
    This function updates an existing person in the people list

    :param person_id: id of the person to update in the people list
    :param person:  person to update
    :return: updated person structure
    """
    # Get the person requested
    update_person = Person.query.filter(Person.person_id==person_id).one_or_none()

    # Try to find an existing person with the same name as update
    lname = person.get("lname", None)
    fname = person.get("fname", None)

    existing_person = Person.query.filter(Person.fname == fname).filter(Person.lname == lname).one_or_none()

    # Are we trying to update a person that does not exist?
    if update_person is None:
        abort(
            404, "Person with person id {person_id} not found".format(person_id=person_id)
        )

    # Will our update create a duplicate person?
    elif existing_person is not None and existing_person.person_id != person_id:
        abort(
            406, "Person {fname} {lname} already exists".format(fname=fname, lname=lname)
        )

    # Otherwise go ahead and update
    else:
        # Convert the passed in person into a db object
        person_schema = PersonSchema()
        update = person_schema.load(person, session=db.session)

        # set the id to the person we want to update
        update.person_id = update_person.person_id

        # merge the new object into the old and commit it
        db.session.merge(update)
        db.session.commit()

        # retrun the updated person in response
        data = person_schema.dump(update_person)
        return data, 200


def delete(person_id):
    """
    This function deletes a person from the people list

    :param person_id: id of the person to delete
    :return: 200 on successful delete, 404 if not found
    """
    # Get the person requested
    delete_person = Person.query.filter(Person.person_id==person_id).one_or_none()

    # Does this person exist
    if delete_person is not None:
        db.session.delete(delete_person)
        db.session.commit()
        return make_response(
            "Person {person_id} successfully deleted".format(person_id=person_id), 200
        )

    else:
        abort(
            404, "Person with person id {person_id} not found".format(person_id=person_id)
        )