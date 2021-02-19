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

    # test the GET method in /shelters/ returns all the shelters
    def test_get_all_shelters(self):
        response = self.client.get("/shelters/")

        data = response.get_json()
        #check the OK status
        self.assertEqual(response.status_code, 200)
        #the response data is a list
        self.assertIsInstance(data, list)
        #the length of the list is 2, we know that because we seeded the data
        self.assertEqual(len(data), 2)

    def test_get_shelters_by_id(self):
        #get the first shelter from the db -> id=1
        shelter = Shelter.query.first()
        response = self.client.get(f"/shelters/{shelter.id}")

        data = response.get_json()
         #check the OK status
        self.assertEqual(response.status_code, 200)
        #the response data is a dict
        self.assertIsInstance(data, dict)
        #test a value of the response, as we seeded the data we know that value
        self.assertEqual(data['city'], "Brisbane")
    
    def test_get_animals_by_shelter(self):
         #get the first shelter from the db -> id=1
        shelter = Shelter.query.first()
        response = self.client.get(f"/shelters/{shelter.id}/animals")

        data = response.get_json()
         #check the OK status
        self.assertEqual(response.status_code, 200)
        #the response data is a list
        self.assertIsInstance(data, list)
        #test the length of the list
        self.assertEqual(len(data), 2)

    #POST method in shelters
    def test_post_shelter_create(self):
        #register and login a user
        response = self.client.post("/auth/register", 
        json= {
            "username": "tester",
            "password": "123456"
        })
        #login the user
        response = self.client.post("/auth/login", 
        json= {
            "username": "tester",
            "password": "123456"
        })
        # get the response (token)
        data = response.get_json()
        # store the token to send it in the POST shelter
        headers_data = {
            'Authorization': f"Bearer {data['token']}"
        }
        #creating the data for the shelter
        shelter_data = {
            "name" : "Melbourne Shelter",
            "address": "Main Street",
            "city": "Melbourne",
            "phone": "1800333444",
            "email": "mlb@mlbshelter.com"
        }
        # the POST request with the url, the shelter data and the token
        response = self.client.post("shelters/",
        json = shelter_data,
        headers = headers_data)
        #get the JSON object of the new shelter
        data = response.get_json()
        #check if we now have a shelter with that ID in the shelters table
        shelter = Shelter.query.get(data["id"])
        #test the 200 status
        self.assertEqual(response.status_code, 200)
        #test there's some data in the response
        self.assertIsNotNone(shelter)
        self.assertEqual(shelter.city, "Melbourne")
    
    #POST method in /shelters not allowed
    def test_post_shelter_create_not_allowed(self):
        #login a user that already exists and get the token
        #login the user
        response = self.client.post("/auth/login", 
        json= {
            "username": "Jairo",
            "password": "123456"
        })
        # get the response (token)
        data = response.get_json()
        # store the token to send it in the POST shelter
        headers_data = {
            'Authorization': f"Bearer {data['token']}"
        }
        #creating the data for the shelter
        shelter_data = {
            "name" : "Melbourne Shelter",
            "address": "Main Street",
            "city": "Melbourne",
            "phone": "1800333444",
            "email": "mlb@mlbshelter.com"
        }
        # the POST request with the url, the shelter data and the token
        response = self.client.post("shelters/",
        json = shelter_data,
        headers = headers_data)

        #test a 400 status, a user that already has a shelter cannot post a new one
        self.assertEqual(response.status_code, 400)

    #DELETE method in shelters/id, not allowed to delete
    def test_delete_shelter_not_allowed(self):
        #register and login a user
        response = self.client.post("/auth/register", 
        json= {
            "username": "tester",
            "password": "123456"
        })
        #login the user
        response = self.client.post("/auth/login", 
        json= {
            "username": "tester",
            "password": "123456"
        })
        # get the response (token)
        data = response.get_json()
        # store the token to send it in the POST shelter
        headers_data = {
            'Authorization': f"Bearer {data['token']}"
        }
        shelter = Shelter.query.first()
        response = self.client.delete(f"shelters/{shelter.id}",
        json = data,
        headers = headers_data)
        #test a 400 status, a user is not the owner of the shelter cannot delete it
        self.assertEqual(response.status_code, 400)

    #DELETE method on /shelters/id allowed
    def test_delete_shelter_allowed(self):
        #login a user that already exists and get the token
        #login the user
        response = self.client.post("/auth/login", 
        json= {
            "username": "Jairo",
            "password": "123456"
        })
        # get the response (token)
        data = response.get_json()
        # store the token to send it in the POST shelter
        headers_data = {
            'Authorization': f"Bearer {data['token']}"
        }

        shelter = Shelter.query.first()
        response = self.client.delete(f"shelters/{shelter.id}",
        json = data,
        headers = headers_data)
        #test the OK status
        self.assertEqual(response.status_code, 200)
        #query to the shelter we deleted
        shelter_del = Shelter.query.get(shelter.id)
        #test that none has been received
        self.assertIsNone(shelter_del)


