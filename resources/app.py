import datetime
from flask import request, jsonify, make_response
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from werkzeug.exceptions import BadRequest

from models import Person, db, app, User

db.init_app(app)  # Initialize the DB
jwt = JWTManager(app)

class PersonSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        include_relationships = True
        load_instance = True


# post endpoint
@app.route('/api/v1/person/create', methods=['POST'])
@jwt_required()
def create():
    data = request.get_json()
    schema = PersonSchema()
    new_person = schema.load(data, session=db.session)
    new_person.create()
    return schema.dump(new_person), HTTPStatus.CREATED


# get endpoint
@app.route('/api/v1/person/list', methods=['GET'])
def index():
    get_person = Person.query.all()
    person_schema = PersonSchema(many=True)
    persons = person_schema.dump(get_person)
    return make_response(jsonify({"response": persons}), HTTPStatus.OK)


@app.route('/api/v1/person/<personId>', methods=['GET'])
def get_person_by_id(personId):
    get_person = Person.query.get(personId)
    person_schema = PersonSchema()
    persons = person_schema.dump(get_person)
    return make_response(jsonify({"response": persons}), HTTPStatus.OK)


# put endpoint
@app.route('/api/v1/person/update/<personId>', methods=['PUT'])
@jwt_required()
def update_person_by_id(personId):
    data = request.get_json()
    get_person = Person.query.get(personId)
    if data.get('personName'):
        get_person.personName = data['personName']
    if data.get('address'):
        get_person.address = data['address']
    get_person.create()
    person_schema = PersonSchema(only=['personId', 'personName', 'address'])
    persons = person_schema.dump(get_person)
    return make_response(jsonify({"response": persons}), HTTPStatus.OK)


# delete endpoint
@app.route('/api/v1/person/delete/<personId>', methods=['DELETE'])
@jwt_required()
def delete_person_by_id(personId):
    persons = Person.query.get(personId)
    persons.create()
    return make_response(jsonify({"response": "SUCCESS"}), HTTPStatus.OK)


@app.route('/api/v1/person/signup', methods=['POST'])
def signup():
    body = request.get_json()
    user = User(email=body.get('email'), password=generate_password_hash(body.get('password')))
    user.create()
    return make_response({'response': {'id': str(user.id), 'email': str(user.email)}}, HTTPStatus.OK)


@app.route('/api/v1/person/token', methods=['POST'])
def login():
    body = request.get_json()
    emailid = body.get('email')
    passwd = body.get('password')
    user = User.query.filter_by(email=emailid).first()

    if (user is not None) and check_password_hash(user.password, passwd):
        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(days=1))
        return make_response({'access_token': access_token}, HTTPStatus.OK)

    raise BadRequest("Invalid Username or password")


if __name__ == '__main__':
    app.run(debug=True, port=8000)
