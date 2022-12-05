import json
import unittest
import requests
from app import app
from models import db

url = 'http://127.0.0.1:8000'  # The root url of the flask app
person = json.dumps({"personName": "Raghavendra", "address": "India"})
user = json.dumps({"email":"uaanti@gmail.com","password":"terenaam"})
token = ""

class testApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db

    def test_endpoint(self):
        lists = requests.get(url + '/api/v1/person/list')  # Passing the urls of flask app
        self.assertEqual(lists.status_code, 200)

    def test_signup(self):
        signup_response = self.app.post('/api/v1/person/signup', headers={"Content-Type": "application/json"}, data=user)
        print(signup_response)
        self.assertEqual(200, signup_response.status_code)

    def test_create(self):
        testing = app.test_client()
        r = testing.post('/api/v1/person/create', data=person)
        assert r.status_code == 401
