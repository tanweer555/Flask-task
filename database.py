from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from urllib.parse import quote_plus


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:%s@localhost/person" % quote_plus("Tanweer@123")
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()