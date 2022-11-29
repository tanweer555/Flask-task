import uuid
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from urllib.parse import quote_plus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:%s@localhost/person" % quote_plus("Tanweer@123")
app.config["JWT_SECRET_KEY"] = "super-secret"
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = "person"
    personId = db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    personName = db.Column(db.String(20))
    address = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, personName, address):
        self.personName = personName
        self.address = address

    def __repr__(self):
        return f"{self.personId}"


class User(db.Model):
    __tablename__ = "user"
    id =  db.Column(db.String(80), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)  # check for min length

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f"{self.id}"


with app.app_context():
    db.create_all()
