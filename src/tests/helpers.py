import unittest, os
from main import create_app, db

class Helpers(unittest.TestCase):
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
        result = runner.invoke(args=["db-custom", "seed"])
        if result.exit_code != 0:
            raise ValueError(result.stdout)
    
    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
    
    @classmethod
    def register(cls, data):
        response = cls.client.post("/auth/register", json=data)
        data = response.get_json()
        return response, data
    
    @classmethod
    def login(cls, data):
        response = cls.client.post("/auth/login", json=data)
        data = response.get_json()
        headers_data = {
            "Authorization" : f"Bearer {data['token']}"
        }
        return headers_data
    
    @classmethod
    def get_request(cls, endpoint, headers=None):
        response = cls.client.get(endpoint, headers=headers)
        data = response.get_json()
        return response, data
    
    @classmethod
    def post_request(cls, endpoint, headers=None, body=None):
        response = cls.client.post(endpoint, headers=headers, json=body)
        data = response.get_json()
        return response, data
    
    @classmethod
    def patch_request(cls, endpoint, headers, body):
        response = cls.client.patch(endpoint, headers=headers, json=body)
        data = response.get_json()
        return response, data

    @classmethod
    def delete_request(cls, endpoint, headers):
        response = cls.client.delete(endpoint, headers=headers)
        data = response.get_json()
        return response, data