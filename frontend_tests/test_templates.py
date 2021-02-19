import unittest
import os
from models.Shelter import Shelter
from main import create_app, db

class TestShelters(unittest.TestCase):
    #Runs before the tests
    @classmethod
    def setUp(cls):
        if os.environ.get("FLASK_ENV") != "testing":
            raise EnvironmentError("FLASK_ENV is not testing")
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()

        db.create_all()

        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db", "seed"])

    #runs after all the tests, removes the tables and stops the app
    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    #GET method in /shelters/
    def test_shelter_index(self):
        #response is going to contain the html with all the shelters
        response = self.client.get("/shelters/")
        #print(response.data)
        #get all the shelters from the database
        shelters = Shelter.query.all()
        #print(shelters[0].city)
        self.assertEqual(response.status_code, 200)
        #test if we have the title of the html in the content of the response
        self.assertIn("Shelters", str(response.data))
        #test content from the layout
        self.assertIn("Welcome", str(response.data))
        #test if the html contains the names and cities of the shelters
        self.assertIn(shelters[0].city, str(response.data))
        self.assertIn(shelters[1].city, str(response.data))
        self.assertIn(shelters[0].name, str(response.data))
        self.assertIn(shelters[1].name, str(response.data))

    def test_shelter_by_id(self):
        shelter = Shelter.query.first()
        response = self.client.get(f"/shelters/{shelter.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Back", str(response.data))
        self.assertIn("Email", str(response.data))
        self.assertIn(shelter.phone, str(response.data))
        self.assertIn(shelter.email, str(response.data))
        self.assertIn(shelter.address, str(response.data))