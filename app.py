from flask import request, jsonify, make_response
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from flask_marshmallow import Marshmallow
import Models
import database
from database import db

ma = Marshmallow(database.app)


class PersonSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Models.Person
        include_relationships = True
        load_instance = True


# post endpoint
@database.app.route('/api/v1/person/create', methods=['POST'])
def create():
    # id = request.get_json('personId')
    # # name = person.get('personName')
    # # address = person.get ('address')
    #
    # existing_username = Person.query.filter(Person.id == id).one_or_none()
    #
    # if existing_username is None:
    data = request.get_json()
    schema = PersonSchema()
    new_person = schema.load(data, session=db.session)
    db.session.add(new_person)
    db.session.commit()
    return schema.dump(new_person), 201

# get endpoint
@database.app.route('/api/v1/list', methods=['GET'])
def index():
    get_person = Models.Person.query.all()
    person_schema = PersonSchema(many=True)
    persons = person_schema.dump(get_person)
    return make_response(jsonify({"response": persons}))


@database.app.route('/api/v1/person/<personId>', methods=['GET'])
def get_person_by_id(personId):
    get_person = Models.Person.query.get(personId)
    person_schema = PersonSchema()
    persons = person_schema.dump(get_person)
    return make_response(jsonify({"response": persons}))


# put endpoint
@database.app.route('/api/v1/person/update/<personId>', methods=['PUT'])
def update_person_by_id(personId):
    data = request.get_json()
    get_person = Models.Person.query.get(personId)
    if data.get('personName'):
        get_person.personName = data['personName']
    if data.get('address'):
        get_person.address = data['address']
    db.db.session.add(get_person)
    db.db.session.commit()
    person_schema = PersonSchema(only=['personId', 'personName', 'address'])
    persons = person_schema.dump(get_person)

    return make_response(jsonify({"response": persons}))


# delete endpoint
@database.app.route('/api/v1/person/delete/<personId>', methods=['DELETE'])
def delete_person_by_id(personId):
    get_person = Models.Person.query.get(personId)
    db.session.delete(get_person)
    db.session.commit()
    return make_response("Deleted", 200)

if __name__ == '__main__':
    database.app.run(debug=True)