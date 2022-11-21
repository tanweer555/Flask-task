from database import db

class Person(db.Model):
    __tablename__ = "person"
    personId = db.Column(db.Integer, primary_key=True)
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
    